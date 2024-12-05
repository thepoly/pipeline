from django.shortcuts import render, redirect, get_object_or_404
from django.urls import path
from django.utils.html import strip_tags
from django.contrib import messages
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from postline.models import PostlinePage  # Changed import
from postline.forms import InstagramPostForm  # Create a form for handling the content
from core.models import ArticlePage
from django.conf import settings
from PIL import Image, ImageDraw, ImageFont
import os
import uuid
import io
import zipfile


def display_articles_table(request):
    # Fetch all articles
    articles = ArticlePage.objects.live().order_by('-date')
    return render(request, 'postline/table.html', {
        'articles': articles,
        'user_has_permission': request.user.has_perm('postline.add_postlinepage')
    })


def create_instagram_post(request, article_id):
    article = get_object_or_404(ArticlePage, id=article_id)
    paragraphs = [
        strip_tags(block.value.source) 
        for block in article.body 
        if block.block_type == 'paragraph'
    ]
    paragraph_choices = [(str(idx), para) for idx, para in enumerate(paragraphs, start=1)]
    
    if request.method == 'POST':
        form = InstagramPostForm(request.POST, paragraphs=paragraph_choices)
        if form.is_valid():
            add_all = form.cleaned_data.get('add_all_paragraphs')
            selected_paragraphs = form.cleaned_data.get('paragraph') if not add_all else list(map(str, range(1, len(paragraphs)+1)))
            
            appended_paragraphs = []
            if add_all:
                appended_paragraphs = paragraphs
            elif selected_paragraphs:
                for selected in selected_paragraphs:
                    para_num = int(selected)
                    if 1 <= para_num <= len(paragraphs):
                        appended_paragraphs.append(paragraphs[para_num - 1])
                    else:
                        messages.warning(request, f'Invalid paragraph selection: {selected}. Ignoring.')
            
            generated_images = []
            if appended_paragraphs:
                for idx, para in enumerate(appended_paragraphs, start=1):
                    image_filename = generate_image_from_text(para, article_id, idx)
                    if image_filename:
                        image_url = settings.MEDIA_URL + image_filename
                        generated_images.append(image_url)
                        
            if generated_images:
                return render(request, 'postline/generated_images.html', {
                    'generated_images': generated_images,
                })
            else:
                messages.warning(request, 'No images were generated.')
                return redirect('postline:display_articles_table')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = InstagramPostForm(paragraphs=paragraph_choices)
    
    return render(request, 'postline/create_post.html', {
        'form': form,
        'article': article,
    })

import logging

logger = logging.getLogger(__name__)

def generate_image_from_text(text, article_id, image_number):
    try:
        img_width = 1080
        img_height = 1080
        background_color = (255, 255, 255)
        
        image = Image.new('RGB', (img_width, img_height), color=background_color)
        draw = ImageDraw.Draw(image)
        
        font_path = os.path.join(settings.BASE_DIR, 'postline', 'fonts', 'Raleway-Regular.ttf')
        font_size = 40
        try:
            font = ImageFont.truetype(font_path, font_size)
        except IOError:
            font = ImageFont.load_default()
        
        text_color = (0, 0, 0)
        margin = 50
        max_width = img_width - 2 * margin
        lines = text_wrap(text, font, max_width)
        
        line_height = (font.getbbox('A')[3] - font.getbbox('A')[1]) + 10
        total_text_height = line_height * len(lines)
        current_y = (img_height - total_text_height) // 2
        
        for line in lines:
            draw.text((margin, current_y), line, font=font, fill=text_color)
            current_y += line_height
        
        filename = f"article_{article_id}_image{image_number}.png"
        upload_path = os.path.join('instagram_posts', filename)
        full_path = os.path.join(settings.MEDIA_ROOT, upload_path)
        
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        image.save(full_path, format='PNG')
        
        return upload_path
    except Exception as e:
        logger.error(f"Error generating image: {e}")
        return None

def text_wrap(text, font, max_width):
    """
    Wraps text for the image to ensure it fits within the specified width.
    Returns a list of lines.
    """
    lines = []
    
    if (font.getbbox(text)[2] - font.getbbox(text)[0]) <= max_width:
        lines.append(text)
    else:
        words = text.split(' ')
        i = 0
        while i < len(words):
            line = ''
            while i < len(words):
                # Calculate the width of the current line with the next word
                test_line = f"{line}{words[i]} "
                line_width = font.getbbox(test_line)[2] - font.getbbox(test_line)[0]
                
                if line_width <= max_width:
                    line = test_line
                    i += 1
                else:
                    break
            if not line:
                # Split the word if it's longer than max_width
                line = words[i]
                i += 1
            lines.append(line)
    return lines


@login_required
@require_POST
def download_all_images(request):
    image_urls = request.POST.getlist('image_urls')
    
    if not image_urls:
        messages.error(request, 'No images available for download.')
        return redirect('postline:display_articles_table')
    
    # Create a BytesIO buffer to hold the zip file in memory
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        for image_url in image_urls:
            # Remove MEDIA_URL from the image_url to get the relative path
            if image_url.startswith(settings.MEDIA_URL):
                relative_path = image_url.replace(settings.MEDIA_URL, '')
                file_path = os.path.join(settings.MEDIA_ROOT, relative_path)
                
                if os.path.exists(file_path):
                    # Add the file to the zip archive
                    zip_file.write(file_path, arcname=os.path.basename(file_path))
                else:
                    messages.warning(request, f'File not found: {relative_path}')
            else:
                messages.warning(request, f'Invalid URL: {image_url}')
    
    if zip_buffer:
        zip_buffer.seek(0)
        response = HttpResponse(zip_buffer, content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename=generated_images.zip'
        return response
    else:
        messages.error(request, 'Failed to create zip file.')
        return redirect('postline:display_articles_table')