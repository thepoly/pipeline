from django.db import models

from wagtail.core.models import Page
from wagtail.admin.edit_handlers import PageChooserPanel


class HomePage(Page):
    featured_article = models.ForeignKey(
        'articles.ArticlePage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text='Article that is displayed prominently at the top of the home page.'
    )

    content_panels = Page.content_panels + [
        PageChooserPanel('featured_article'),
    ]
