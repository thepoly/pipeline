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
    title = article.title
    summary = strip_tags(article.summary)

    # Extract paragraphs from the article
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
            generate_title_image = form.cleaned_data.get('generate_title_image')
            extra_text = form.cleaned_data.get('extra_text', "").strip()  # Remove any unnecessary whitespace
            extra_text_position = form.cleaned_data.get('extra_text_position', "left")

            selected_paragraphs = form.cleaned_data.get('paragraph') if not add_all else list(map(str, range(1, len(paragraphs) + 1)))
            generated_images = []

            # First image: Title + Summary
            if generate_title_image:
                first_image = generate_image_from_text(
                    title=title,
                    content=summary,
                    extra_text=extra_text,
                    extra_text_position=extra_text_position,
                    article_id=article_id,
                    image_number=1,
                    is_first_image=True
                )
                if first_image:
                    generated_images.append(settings.MEDIA_URL + first_image)

            # Remaining images: Paragraphs
            for idx, paragraph in enumerate(paragraphs, start=1):
                if add_all or str(idx) in selected_paragraphs:
                    image_filename = generate_image_from_text(
                        title=None,  # No title for subsequent images
                        content=paragraph,
                        extra_text=extra_text,
                        extra_text_position=extra_text_position,
                        article_id=article_id,
                        image_number=idx + 1,
                        is_first_image=False
                    )
                    if image_filename:
                        generated_images.append(settings.MEDIA_URL + image_filename)

            if generated_images:
                return render(request, 'postline/generated_images.html', {'generated_images': generated_images})
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
        'has_paragraphs': bool(paragraphs)
    })

import logging

logger = logging.getLogger(__name__)

def generate_image_from_text(title=None, content="", extra_text="", extra_text_position="left", article_id=None, image_number=1, is_first_image=False):
    try:
        img_width = 1080
        img_height = 1080
        background_color = (255, 255, 255)

        # Create a blank image
        image = Image.new('RGB', (img_width, img_height), color=background_color)
        draw = ImageDraw.Draw(image)

        # Fonts
        font_path_italic = os.path.join(settings.BASE_DIR, 'postline', 'fonts', 'Raleway-Italic.ttf')
        font_path_bold_italic = os.path.join(settings.BASE_DIR, 'postline', 'fonts', 'Raleway-BoldItalic.ttf')
        font_path_black_italic = os.path.join(settings.BASE_DIR, 'postline', 'fonts', 'Raleway-BlackItalic.ttf')
        font_size_title = 60
        font_size_summary = 38
        font_size_extra_text = 200
        font_size_poly_text = 34

        try:
            title_font = ImageFont.truetype(font_path_bold_italic, font_size_title)
            content_font = ImageFont.truetype(font_path_italic, font_size_summary)
            extra_text_font = ImageFont.truetype(font_path_black_italic, font_size_extra_text)
            poly_text_font = ImageFont.truetype(font_path_bold_italic, font_size_poly_text)
        except IOError:
            title_font = ImageFont.load_default()
            content_font = ImageFont.load_default()
            extra_text_font = ImageFont.load_default()
            poly_text_font = ImageFont.load_default()

        text_color = (218, 30, 5)
        extra_text_color = (246, 218, 215)
        margin = 100
        extra_text_margin = 5
        max_width = img_width - 2 * margin

        if extra_text: # NEW, FEATURES ... etc
            while True:
                text_width, text_height = get_text_size(extra_text, extra_text_font)
                if text_width <= image.width - extra_text_margin:
                    break
                font_size_extra_text -= 5
                extra_text_font = ImageFont.truetype(font_path_black_italic, font_size_extra_text)

            text_img = Image.new('RGBA', (img_height, img_width), (255, 255, 255, 0))
            text_draw = ImageDraw.Draw(text_img)
            text_bbox = text_draw.textbbox((0, 0), extra_text, font=extra_text_font)

            poly_text_width, poly_text_height = get_text_size("The Polytechnic", poly_text_font)
            poly_text_img = Image.new('RGBA', (img_width, img_height), (255, 255, 255, 0))  # Transparent background
            poly_text_draw = ImageDraw.Draw(poly_text_img)
            poly_text_draw.text((0, 0), "the polytechnic", font=poly_text_font, fill=text_color)

            text_x = 10
            text_y = 10
            # Draw the text onto the transparent image
            text_y_offset = text_bbox[1]  # Top offset of the text
            text_draw.text((text_x, text_y - text_y_offset), extra_text, font=extra_text_font, fill=extra_text_color)
            
            # Rotate the text image
            rotated_text_img = text_img.rotate(90, expand=True)
            rotated_poly_text_img = poly_text_img.rotate(90, expand=True)
            
            # Paste the rotated text onto the main image
            if extra_text_position == "left":
                image.paste(rotated_text_img, (0, 0), rotated_text_img)
                print(poly_text_width)
                image.paste(rotated_poly_text_img, (img_width - poly_text_height - text_x, 0 - (img_height - poly_text_width - text_y)), rotated_poly_text_img)
            elif extra_text_position == "right":
                image.paste(rotated_text_img, (img_width - text_height - (2 * text_x), 0 - text_y), rotated_text_img)
                image.paste(poly_text_img, (0 + text_x, img_height - poly_text_height - text_y), poly_text_img)

        # Combine title and content
        combined_lines = []
        if is_first_image and title:
            combined_lines += text_wrap(title, title_font, max_width)
            combined_lines.append("")
            combined_lines.append("")
        combined_lines += text_wrap(content, content_font, max_width)

        # Calculate total height of the text and center it
        line_height = max(
            (title_font.getbbox('A')[3] - title_font.getbbox('A')[1]),
            (content_font.getbbox('A')[3] - content_font.getbbox('A')[1])
        ) + 10
        total_text_height = line_height * len(combined_lines)
        current_y = (img_height - total_text_height) // 2

        # Draw text
        for line in combined_lines:
            font = title_font if line in combined_lines[:len(combined_lines) - len(text_wrap(content, content_font, max_width))] else content_font
            draw.text((margin, current_y), line, font=font, fill=text_color)
            current_y += line_height

        # Save the image
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

def get_text_size(text, font):
    bbox = font.getbbox(text)
    text_width = bbox[2] - bbox[0]  # x_max - x_min
    text_height = bbox[3] - bbox[1]  # y_max - y_min
    return text_width, text_height
