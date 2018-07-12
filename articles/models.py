from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.blocks import RichTextBlock
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel

from bs4 import BeautifulSoup


class ArticlePage(Page):
    headline = RichTextField(features=['italic'])
    date = models.DateField()
    body = StreamField([
        ('paragraph', RichTextBlock()),
    ])

    content_panels = [
        FieldPanel('headline'),
        FieldPanel('date'),
        StreamFieldPanel('body'),
    ]

    def clean(self):
        super().clean()

        soup = BeautifulSoup(self.headline)
        self.title = soup.text


class ArticlesIndex(Page):
    subpage_types = ['ArticlePage']
