from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.blocks import RichTextBlock
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel, InlinePanel, PageChooserPanel
from wagtail.snippets.models import register_snippet
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from modelcluster.fields import ParentalKey

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
        ('image', ImageChooserBlock()),
    ])
    summary = RichTextField(
        features=['italic'],
        null=True,
        blank=True,
        help_text='Displayed on the home page or other places to provide a taste of what the article is about.'
    )
    featured_photo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        help_text='Shown at the top of the article and on the home page.'
    )

    content_panels = [
        MultiFieldPanel([
                FieldPanel('headline', classname="title"),
                FieldPanel('subdeck'),
            ]),
        MultiFieldPanel([
                FieldPanel('date'),
                # TODO: use https://github.com/wagtail/wagtail-autocomplete for kicker
                SnippetChooserPanel('kicker'),
                InlinePanel('article_author_relationship', label='Author', min_num=1),
                ImageChooserPanel('featured_photo'),
            ],
            heading='Metadata',
            classname='collapsible'),
        FieldPanel('summary'),
        StreamFieldPanel('body'),
    ]

    search_fields = Page.search_fields + [
        index.SearchField('headline'),
        index.SearchField('subdeck'),
        index.SearchField('body'),
        index.SearchField('summary'),
    ]

    def clean(self):
        super().clean()

        soup = BeautifulSoup(self.headline, 'html.parser')
        self.title = soup.text
    
    def authors(self):
        return [r.author for r in self.article_author_relationship.all()]


class ArticlesIndexPage(Page):
    subpage_types = ['ArticlePage']

    def get_articles(self):
        return ArticlePage.objects.live().descendant_of(self).order_by('date')


@register_snippet
class Kicker(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class ArticleAuthorRelationship(models.Model):
    article = ParentalKey('ArticlePage', related_name='article_author_relationship', on_delete=models.PROTECT)
    author = models.ForeignKey('authors.AuthorPage', related_name='author_article_relationship', on_delete=models.PROTECT)
    title = RichTextField(
        features=['italic'],
        null=True,
        blank=True
    )

    panels = [
        PageChooserPanel('author'),
        FieldPanel('title'),
    ]
