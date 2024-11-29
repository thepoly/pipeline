from django.shortcuts import render, redirect, get_object_or_404
from django.urls import path
from django.utils.html import strip_tags
from django.contrib import messages
from postline.models import PostlinePage  # Changed import
from postline.forms import InstagramPostForm  # Create a form for handling the content
from core.models import ArticlePage
from django.conf import settings
from PIL import Image, ImageDraw, ImageFont
import os
import uuid

def display_articles_table(request):
    # Fetch all articles
    articles = ArticlePage.objects.live().order_by('-date')
    return render(request, 'postline/table.html', {
        'articles': articles,
        'user_has_permission': request.user.has_perm('postline.add_postlinepage')
    })


def create_instagram_post(request, article_id):
    article = get_object_or_404(ArticlePage, id=article_id)
    
    # Extract paragraphs from the StreamField
    paragraphs = [
        strip_tags(block.value.source) 
        for block in article.body 
        if block.block_type == 'paragraph'
    ]
    
    # Prepare choices for the multiple choice field
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
                for para in appended_paragraphs:
                    image_filename = generate_image_from_text(para)
                    if image_filename:
                        image_url = settings.MEDIA_URL + image_filename
                        generated_images.append(image_url)
                        
                        # Create a PostlinePage instance for each image
                        
                        postline_page = PostlinePage(
                            title=f"Instagram Post for {article.title} - {uuid.uuid4().hex[:6]}",
                            posted=False,
                            instagram_link='',  # To be updated after actual Instagram API integration
                            article=article,
                            image=image_filename
                        )
                        parent_page = article.get_parent().specific  # Ensure correct page type
                        parent_page.add_child(instance=postline_page)
            
            if generated_images:
                # Pass the list of image URLs to the template for download/display
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

def generate_image_from_text(text):
    """
    Generates an image from the provided text and saves it to MEDIA_ROOT/instagram_posts/.
    Returns the relative path to the saved image.
    """
    try:
        # Image configuration
        img_width = 1080
        img_height = 1080
        background_color = (255, 255, 255)  # White background
        
        # Create a new image
        image = Image.new('RGB', (img_width, img_height), color=background_color)
        draw = ImageDraw.Draw(image)
        
        # Define font and size
        font_path = os.path.join(settings.BASE_DIR, 'postline', 'fonts', 'arial.ttf')  # Ensure correct path
        font_size = 40
        try:
            font = ImageFont.truetype(font_path, font_size)
        except IOError:
            font = ImageFont.load_default()
        
        # Text settings
        text_color = (0, 0, 0)  # Black text
        margin = 50
        max_width = img_width - 2 * margin
        lines = text_wrap(text, font, max_width)
        
        # Calculate text height to center vertically
        line_height = (font.getbbox('A')[3] - font.getbbox('A')[1]) + 10
        total_text_height = line_height * len(lines)
        current_y = (img_height - total_text_height) // 2
        
        for line in lines:
            draw.text((margin, current_y), line, font=font, fill=text_color)
            current_y += line_height
        
        # Generate unique filename
        filename = f"{uuid.uuid4().hex}.png"
        upload_path = os.path.join('instagram_posts', filename)
        full_path = os.path.join(settings.MEDIA_ROOT, upload_path)
        
        # Ensure the directory exists
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        # Save the image
        image.save(full_path, format='PNG')
        
        return upload_path  # Relative path from MEDIA_ROOT
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