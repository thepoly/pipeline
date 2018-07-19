from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.blocks import RichTextBlock
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel
from wagtail.snippets.models import register_snippet
from wagtail.snippets.edit_handlers import SnippetChooserPanel

from bs4 import BeautifulSoup


class ArticlePage(Page):
    headline = RichTextField(features=['italic'])
    subdeck = RichTextField(
        features=['italic'],
        null=True,
        blank=True
    )
    kicker = models.ForeignKey(
        'articles.Kicker',
        null=True,
        on_delete=models.PROTECT)
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
            ],
            heading='Front matter'),
        MultiFieldPanel([
                FieldPanel('date'),
                # TODO: use https://github.com/wagtail/wagtail-autocomplete for kicker
                SnippetChooserPanel('kicker'),
            ],
            heading='Metadata'),
        FieldPanel('summary'),
        StreamFieldPanel('body'),
    ]

    def clean(self):
        super().clean()

        soup = BeautifulSoup(self.headline)
        self.title = soup.text


class ArticlesIndex(Page):
    subpage_types = ['ArticlePage']


@register_snippet
class Kicker(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title
