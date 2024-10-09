from django.apps import apps
from django.core.paginator import Paginator
from django.db import models
from django.db.models import F, Max
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from django.http import Http404
from django.shortcuts import render
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.html import format_html, mark_safe
from django.utils.text import slugify

# Create your models here.
from django.templatetags.static import static
from django.utils.html import format_html
from wagtail.admin import widgets as wagtailadmin_widgets

from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.blocks import (
    RichTextBlock,
    ListBlock,
    StructBlock,
    URLBlock,
    StructValue,
    ChoiceBlock,
)
from modelcluster.fields import ParentalKey

from wagtail.admin.panels import (
    FieldPanel,
    MultiFieldPanel,
    InlinePanel,
    PageChooserPanel,
)
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField, StreamField

from wagtail.fields import RichTextField, StreamField
from wagtail.models import Page, Orderable

from wagtail.embeds.embeds import get_embed
from wagtail.embeds.blocks import EmbedBlock
from wagtail.search import index
from wagtail.snippets.blocks import SnippetChooserBlock
from wagtail.snippets.models import register_snippet
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.models import Image, AbstractImage, AbstractRendition
# from wagtailautocomplete.panels import AutocompletePanel
from modelcluster.fields import ParentalKey, ParentalManyToManyField


from django import forms
from django.utils.encoding import force_str
from django.utils.html import format_html
from wagtail.blocks import FieldBlock

class ArticlesIndexPage(RoutablePageMixin, Page):
    subpage_types = ["ArticlePage"]

    @route(r"^(\d{4})\/(\d{2})\/(.*)\/$")
    def post_by_date(self, request, year, month, slug, *args, **kwargs):
        try:
            page = ArticlePage.objects.live().get(
                slug=slug,
                first_published_at__year=year,
                first_published_at__month=month,
            )
        except ArticlePage.DoesNotExist:
            raise Http404
        return page.serve(request, *args, **kwargs)

    def get_articles(self):
        return (
            ArticlePage.objects.live()
            .descendant_of(self)
            .order_by("-first_published_at")
            # .select_related("featured_image")
        )

    def get_context(self, request):
        context = super().get_context(request)
        paginator = Paginator(self.get_articles(), 24)
        page = request.GET.get("page")
        context["articles"] = paginator.get_page(page)
        return context

class ArticlePage(RoutablePageMixin, Page):
    date = models.DateField("Post date")
    kicker = models.CharField(max_length=250)
    body = RichTextField(blank=True)
    # featured_image = models.ForeignKey(
    #     "wagtailimages.Image",
    #     null=True,
    #     blank=True,
    #     on_delete=models.SET_NULL,
    #     related_name="+",
    # )

    search_fields = Page.search_fields + [
        index.SearchField("kicker"),
        index.SearchField("body"),
    ]

    content_panels = Page.content_panels + [
        FieldPanel("date"),
        FieldPanel("kicker"),
        FieldPanel("body"),
        # ImageChooserPanel("featured_image"),
        # FieldPanel("featured_image"),
    ]

    parent_page_types = ["ArticlesIndexPage"]

    def get_context(self, request):
        context = super().get_context(request)
        context["related_articles"] = (
            ArticlePage.objects.live()
            .exclude(id=self.id)
            .filter(kicker=self.kicker)
            .order_by("-first_published_at")[:3]
        )
        return context

@register_snippet
class Kicker(models.Model):
    title = models.CharField(max_length=255)

    @classmethod
    def autocomplete_create(kls: type, value: str):
        return kls.objects.create(title=value)

    def __str__(self):
        return self.title
