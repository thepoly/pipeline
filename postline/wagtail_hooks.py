from django.urls import path, reverse

from wagtail.admin.menu import MenuItem
from wagtail import hooks

from .views import display_articles_table


@hooks.register('register_admin_urls')
def register_postline_url():
    return [
        path('postline/', display_articles_table, name='postline'),
    ]


@hooks.register('register_admin_menu_item')
def register_postline_menu_item():
    return MenuItem('Postline', reverse('postline'), icon_name='tablet-alt')

