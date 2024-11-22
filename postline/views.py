from django.shortcuts import render, redirect, get_object_or_404
from django.urls import path
from django.utils.html import strip_tags
from django.contrib import messages

from core.models import ArticlePage
from postline.models import PostlineIndexPage, PostlinePage  # Changed import
from postline.forms import InstagramPostForm  # Create a form for handling the content

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
    paragraphs = []
    for block in article.body:
        if block.block_type == 'paragraph':
            # Extract plain text by stripping HTML tags
            para_text = strip_tags(block.value.source)
            paragraphs.append(para_text)
    
    # Prepare choices for the multiple choice field
    paragraph_choices = [(str(idx), para) for idx, para in enumerate(paragraphs, start=1)]
    
    if request.method == 'POST':
        form = InstagramPostForm(request.POST, paragraphs=paragraph_choices)
        if form.is_valid():
            caption = form.cleaned_data['caption']
            image_url = form.cleaned_data['image_url']
            scheduled_time = form.cleaned_data.get('scheduled_time')
            add_all = form.cleaned_data.get('add_all_paragraphs')
            selected_paragraphs = form.cleaned_data.get('paragraph') if not add_all else []
            
            appended_paragraphs = []
            
            if add_all:
                appended_paragraphs = paragraphs
            elif selected_paragraphs:
                for selected in selected_paragraphs:
                    try:
                        para_num = int(selected)
                        if 1 <= para_num <= len(paragraphs):
                            appended_paragraphs.append(paragraphs[para_num - 1])
                    except (ValueError, IndexError):
                        messages.warning(request, f'Invalid paragraph selection: {selected}. Ignoring.')
            
            if appended_paragraphs:
                # Append each selected paragraph to the caption
                caption += "\n\n" + "\n\n".join(appended_paragraphs)
            
            # Create a new PostlinePage instance linked to the article
            postline_page = PostlinePage(
                title=f"Instagram Post for {article.title}",
                posted=False,
                instagram_link='',
                article=article  # Ensure ForeignKey in PostlinePage
            )
            
            # Link to the parent PostlineIndexPage
            parent_page = article.get_parent().specific  # Ensure correct page type
            parent_page.add_child(instance=postline_page)
            
            # TODO: Implement Instagram post creation logic here
            # Example:
            # instagram_link = postline_page.create_instagram_post(caption, image_url)
            # if instagram_link:
            #     postline_page.posted = True
            #     postline_page.instagram_link = instagram_link
            #     postline_page.save()
            
            messages.success(request, 'Instagram post created successfully!')
            return redirect('postline:display_articles_table')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = InstagramPostForm(paragraphs=paragraph_choices)
    
    return render(request, 'postline/create_post.html', {
        'form': form,
        'article': article,
    })