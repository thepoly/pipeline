from django.db import models

from wagtail.core.fields import RichTextField
from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.search import index


class AuthorPage(Page):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    biography = RichTextField(null=True, blank=True)

    content_panels = [
        MultiFieldPanel([
            FieldPanel('first_name'),
            FieldPanel('last_name'),
        ], heading="Name"),
        FieldPanel('biography'),
    ]

    search_fields = [
        index.SearchField('first_name'),
        index.SearchField('last_name'),
    ]

    def clean(self):
        super().clean()
        self.title = f'{self.first_name} {self.last_name}'

    def get_articles(self):
        return [r.article for r in self.author_article_relationship.all()]


class AuthorsIndexPage(Page):
    subpage_types = ['AuthorPage']

    def get_authors(self):
        return AuthorPage.objects.live().descendant_of(self).order_by('title')
