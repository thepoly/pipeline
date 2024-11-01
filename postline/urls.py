from django.urls import path
from .views import index, display_table, display_articles_table

urlpatterns = [
    path('', index, name='index'),
    path('table/', display_table, name='display_table'),
    path('articles/', display_articles_table, name='display_articles_table'),
]