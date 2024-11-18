from django.shortcuts import render, redirect, get_object_or_404
from django.urls import path
from django.utils.html import strip_tags


from core.models import ArticlePage
from postline.models import PostlineIndexPage  # Changed import
from postline.forms import InstagramPostForm  # Create a form for handling the content

def display_articles_table(request):
    # Fetch all articles
    articles = ArticlePage.objects.live().order_by('-date')
    return render(request, 'postline/table.html', {
        'articles': articles,
        'user_has_permission': request.user.has_perm('postline.add_postlinepage')
    })

def create_instagram_post(request, article_id):
    # Fetch the article (base model)
    article = get_object_or_404(ArticlePage, id=article_id)

    # Add default behavior for fields if it's not a PostlineIndexPage
    if not isinstance(article, PostlineIndexPage):
        # Dynamically add the Postline fields for compatibility
        article.posted = getattr(article, 'posted', False)
        article.instagram_link = getattr(article, 'instagram_link', None)

    # Rest of your logic remains the same
    if request.method == 'POST':
        form = InstagramPostForm(request.POST)
        if form.is_valid():
            article.posted = True
            article.instagram_link = form.cleaned_data['instagram_link']
            article.save()
            return redirect('postline:display_articles_table')
    else:
        form = InstagramPostForm(initial={
            'title': article.title,
            'summary': strip_tags(article.summary),
            'instagram_link': article.instagram_link,
        })
    
    return render(request, 'postline/create_post.html', {'form': form, 'article': article})