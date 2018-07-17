from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.blocks import RichTextBlock
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel

from bs4 import BeautifulSoup


class ArticlePage(Page):
    headline = RichTextField(features=['italic'])
    subdeck = RichTextField(
        features=['italic'],
        null=True,
        blank=True
    )
    date = models.DateField()
    body = StreamField([
        ('paragraph', RichTextBlock()),
    ])
    summary = RichTextField(
        features=['italic'],
        null=True,
        blank=True,
        help_text='Displayed on the home page or other places to provide a taste of what the article is about.'
    )

    content_panels = [
        MultiFieldPanel([
            FieldPanel('headline'),
            FieldPanel('subdeck'),
        ]),
        FieldPanel('date'),
        FieldPanel('summary'),
        StreamFieldPanel('body'),
    ]

    def clean(self):
        super().clean()

        soup = BeautifulSoup(self.headline)
        self.title = soup.text


class ArticlesIndex(Page):
    subpage_types = ['ArticlePage']
