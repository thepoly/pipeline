from django.db import models
from django.utils.text import slugify

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.snippets.models import register_snippet
from wagtail.search import index


class AuthorPage(Page):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    content_panels = [
        FieldPanel('first_name'),
        FieldPanel('last_name'),
    ]

    search_fields = [
        index.SearchField('first_name'),
        index.SearchField('last_name'),
    ]

    def clean(self):
        super().clean()
        self.title = f'{self.first_name} {self.last_name}'
    
# AuthorPage.slug.default = 'blank-slug'


class AuthorsIndexPage(Page):
    subpage_types = ['AuthorPage']

    def get_authors(self):
        return AuthorPage.objects.live().descendant_of(self).order_by('title')
