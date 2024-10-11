import operator

from bs4 import BeautifulSoup

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
from wagtailautocomplete.edit_handlers import AutocompletePanel
from modelcluster.fields import ParentalKey, ParentalManyToManyField


from django import forms
from django.utils.encoding import force_str
from django.utils.html import format_html
from wagtail.blocks import FieldBlock

class PhotoBlock(StructBlock):
    image = ImageChooserBlock()
    caption = RichTextBlock(features=["italic"], required=False)
    size = ChoiceBlock(
        choices=[("small", "Small"), ("medium", "Medium"), ("large", "Large")],
        default="medium",
        help_text="Width of image in article.",
    )
    class Meta:
        icon = "image"

    def render(self, value, context=None):
        if value:
            return format_html(
                '<figure><img src="{}" alt="{}" /><figcaption>{}</figcaption></figure>',
                value["image"].url,
                value["image"].title,
                value["caption"],
            )
        return ""

class GalleryPhotoBlock(StructBlock):
    image = ImageChooserBlock()
    caption = RichTextBlock(features=["italic"], required=False)

class EmbeddedMediaValue(StructValue):
    def type(self):
        embed_url = self.get("embed").url
        embed = get_embed(embed_url)
        return embed.type

class EmbeddedMediaBlock(StructBlock):
    embed = EmbedBlock(help_text="URL to the content to embed.")
    size = ChoiceBlock(
        choices=[("small", "Small"), ("medium", "Medium"), ("large", "Large")],
        default="medium",
        help_text="Width of video in article.",
    )

    class Meta:
        value_class = EmbeddedMediaValue
        icon = "media"

class CarouselBlock(StructBlock):
    image = ImageChooserBlock()
    
    class Meta:
        icon = "media"

class BlockQuoteBlock(FieldBlock):

    def __init__(self, required=True, help_text=None, max_length=None, min_length=None, **kwargs):
        self.field = forms.CharField(
            required=required,
            help_text=help_text,
            max_length=max_length,
            min_length=min_length
        )
        super(BlockQuoteBlock, self).__init__(**kwargs)

    def get_searchable_content(self, value):
        return [force_str(value)]

    def render_basic(self, value, context=None):
        if value:
            return format_html('<p class="indent">{0}</p>', value)
        else:
            return ''

    class Meta:
        icon = "openquote"

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
    subdeck = RichTextField(features=["italic"], blank=True, null=True)
    date = models.DateField("Post date")
    kicker = models.ForeignKey("Kicker", null=True, blank=True, on_delete=models.PROTECT)
    # body = RichTextField(blank=True)
    body = StreamField(
        [
            ("paragraph", RichTextBlock()),
            ("photo", PhotoBlock()),
            ("photo_gallery", ListBlock(GalleryPhotoBlock(), icon="image")),
            ("embed", EmbeddedMediaBlock()),
            ("carousel", CarouselBlock()),
            ("blockquote", BlockQuoteBlock()),
        ],
        blank=True,
    )
    summary = RichTextField(
        features=["italic"],
        null=True,
        blank=True,
        help_text="Displayed on the home page or other places to provide a taste of what the article is about.",
    )
    featured_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    featured_caption = RichTextField(features=["italic"], blank=True, null=True)


    search_fields = Page.search_fields + [
        index.SearchField("title"),
        index.SearchField("kicker"),
        index.SearchField("body"),
        index.SearchField("get_author_names", partial_match=True),
    ]

    content_panels = Page.content_panels + [
        FieldPanel("subdeck"),
        FieldPanel("date"),
        MultiFieldPanel(
            [
                InlinePanel(
                    "authors",
                    panels=[
                        AutocompletePanel("author", target_model="core.Contributor")
                    ],
                    label="Author",
                ),
                AutocompletePanel("kicker", target_model="core.Kicker"),
                FieldPanel("featured_image"),
                FieldPanel("featured_caption"),
            ],
            heading="Metadata",
            classname="collapsible",
        ),
        FieldPanel("summary"),
        FieldPanel("body"),
        # ImageChooserPanel("featured_image"),
        # FieldPanel("featured_image"),
    ]

    parent_page_types = ["ArticlesIndexPage"]

    def get_context(self, request):
        context = super().get_context(request)
        context["related_articles"] = self.get_related_articles()
        context["authors"] = self.get_authors()
        return context

    def set_url_path(self, parent):
        """Make sure the page knows its own path. The published date might not be set,
        so we have to take that into account and ignore it if so."""
        date = self.get_published_date() or timezone.now()
        self.url_path = f"{parent.url_path}{date.year}/{date.month:02d}/{self.slug}/"
        return self.url_path

    def get_published_date(self):
        return (
            self.date
            or self.go_live_at
            or self.first_published_at
            or getattr(self.get_latest_revision(), "created_at", None)
        )

    def get_authors(self):
        return [r.author for r in self.authors.select_related("author")]

    def get_author_names(self):
        return [a.name for a in self.get_authors()]

    def get_plain_text(self):
        builder = ""
        soup = BeautifulSoup(self.get_text_html(), "html.parser")
        for para in soup.findAll("p"):
            builder += para.text
            builder += " "
        return builder[:-1]

    def get_text_html(self):
        """Get the HTML that represents paragraphs within the article as a string."""
        builder = ""
        for block in self.body:
            if block.block_type == "paragraph":
                builder += str(block.value)
        return builder

    def get_related_articles(self):
        return (
            ArticlePage.objects.live()
            .exclude(id=self.id)
            .filter(path__startswith=self.get_parent().path)
            .order_by("-date")[:4]
        )

class ArticleAuthorRelationship(models.Model):
    article = ParentalKey(ArticlePage, related_name="authors", on_delete=models.CASCADE)
    author = models.ForeignKey("Contributor", related_name="articles", on_delete=models.CASCADE)

    panels = [
        FieldPanel("author"),
    ]

    class Meta:
        unique_together = ("article", "author")

@register_snippet
class Kicker(models.Model):
    title = models.CharField(max_length=255)

    @classmethod
    def autocomplete_create(kls: type, value: str):
        return kls.objects.create(title=value)

    def __str__(self):
        return self.title

@register_snippet
class Contributor(index.Indexed, models.Model):
    name = models.CharField(max_length=255)
    rich_name = RichTextField(features=["italic"], max_length=255, null=True, blank=True)
    id = models.AutoField(primary_key=True)

    search_fields = [index.SearchField("name", partial_match=True)]

    autocomplete_search_field = "name"

    class Meta:
        ordering = ["name"]

    def autocomplete_label(self):
        return self.name

    @classmethod
    def autocomplete_create(kls: type, value: str):
        return kls.objects.create(name=value)

    def get_articles(self):
        return (
            ArticlePage.objects.live()
            .filter(authors__author=self)
            .order_by("-first_published_at")
            .all()
        )
    
    def __str__(self):
        return self.name