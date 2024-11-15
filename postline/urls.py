from django.urls import path
from .views import display_articles_table, create_instagram_post

app_name = 'postline'

urlpatterns = [
    path('articles/', display_articles_table, name='display_articles_table'),
    path('articles/<int:article_id>/create_post/', create_instagram_post, name='create_instagram_post'),
]