from django.urls import path, reverse

from wagtail.admin.menu import MenuItem
from wagtail import hooks

from .views import index


@hooks.register('register_admin_urls')
def register_calendar_url():
    return [
        path('postline/', index, name='postline'),
    ]


@hooks.register('register_admin_menu_item')
def register_calendar_menu_item():
    return MenuItem('Postline', reverse('postline'), icon_name='tablet-alt')