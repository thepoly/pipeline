from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import PageChooserPanel, StreamFieldPanel
from wagtail.core import blocks


class HomePage(Page):
    featured_article = models.ForeignKey(
        'articles.ArticlePage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text='Article that is displayed prominently at the top of the home page.'
    )
    featured_articles = StreamField([
            ('article', blocks.PageChooserBlock(
                target_model='articles.ArticlePage',
                template='home/featured_article_block.html'
            ))
        ],
        null=True
    )

    content_panels = Page.content_panels + [
        PageChooserPanel('featured_article'),
        StreamFieldPanel('featured_articles')
    ]
