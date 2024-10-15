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

class StaticPage(Page):
    body = RichTextField(blank=True, null=True)

    content_panels = Page.content_panels + [FieldPanel("body")]

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
        "core.CustomImage",
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
            .order_by("-date")
            .all()
        )
    
    def __str__(self):
        return self.name

# https://docs.wagtail.org/en/v6.2.2/advanced_topics/images/custom_image_model.html
class CustomImage(AbstractImage):
    photographer = models.ForeignKey(
        "core.Contributor",
        on_delete=models.CASCADE,
        related_name="images",
        blank=True,
        null=True,
    )

    admin_form_fields = Image.admin_form_fields + ("photographer",)

    # TODO: add autocomplete panel for photographer, doesn't work
    # panels = [
    #     AutocompletePanel("photographer", target_model="core.Contributor"),
    # ]

    def get_attribution_html(self):
        if self.photographer is None:
            return ""

        if hasattr(self.photographer, "staff_page"):
            sp = self.photographer.staff_page
            return format_html(
                '<a href="{}">{}</a>/<i>The Polytechnic</i>', sp.url, sp.name
            )

        return self.photographer.name

# Delete the source image file when an image is deleted
@receiver(pre_delete, sender=CustomImage)
def image_delete(sender, instance, **kwargs):
    instance.file.delete(False)


""" # Do feature detection when a user saves an image without a focal point
@receiver(pre_save, sender=CustomImage)
def image_feature_detection(sender, instance, **kwargs):
    # Make sure the image doesn't already have a focal point
    if not instance.has_focal_point():
        # Set the focal point
        instance.set_focal_point(instance.get_suggested_focal_point())
 """

class CustomRendition(AbstractRendition):
    image = models.ForeignKey(
        "core.CustomImage", on_delete=models.CASCADE, related_name="renditions"
    )

    class Meta:
        unique_together = ("image", "filter_spec", "focal_point_key")

# Delete the rendition image file when a rendition is deleted
# TODO: test if this actually works
@receiver(pre_delete, sender=CustomRendition)
def rendition_delete(sender, instance, **kwargs):
    instance.file.delete(False)


class StaffIndexPage(Page):
    subpage_types = ["StaffPage"]

    # create an editable list of positions where the inputs are the position titles and the order matters
    positions = StreamField(
        [("position", SnippetChooserBlock("core.Position"))],
        blank=True,
        help_text="Order matters. The first position is the most important.",
    )

    content_panels = Page.content_panels + [FieldPanel("positions")]


    def get_active_staff(self):
        # take the positions from the stream field and get the activate staff for each position in the order they are in the stream field
        positions = [block.value for block in self.positions]
        staff = []
        for position in positions:
            staff.extend(
                StaffPage.objects.live()
                .descendant_of(self)
                .filter(
                    terms__position=position,
                    terms__date_ended__isnull=True,
                )
                .select_related("photo")
                .prefetch_related("terms__position")
                .distinct()
            )

        return staff  

    def get_previous_staff(self):
        return (
            StaffPage.objects.live()
            .descendant_of(self)
            .exclude(terms__date_ended__isnull=True, terms__position__isnull=False)
            .annotate(latest_term_ended=Max("terms__date_ended"))
            .order_by(F("latest_term_ended").desc(nulls_last=True))
        )

class StaffPage(Page):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    biography = RichTextField(null=True, blank=True)
    photo = models.ForeignKey(
        "core.CustomImage", null=True, blank=True, on_delete=models.SET_NULL, related_name="+"
    )
    email_address = models.EmailField(null=True, blank=True)
    contributor = models.OneToOneField(
        Contributor,
        on_delete=models.SET_NULL, 
        null=True,
        blank=True,
        related_name="staff_page",
    )

    parent_page_types = ["StaffIndexPage"]
    subpage_types = []

    content_panels = [
        MultiFieldPanel(
            [FieldPanel("first_name"), FieldPanel("last_name")], heading="Name"
        ),
        FieldPanel("email_address"),
        FieldPanel("biography"),
        FieldPanel("photo"),
        InlinePanel("terms", label="Term", heading="Terms", min_num=0),
        AutocompletePanel("contributor", target_model="core.Contributor"),
    ]

    search_fields = [index.SearchField("first_name"), index.SearchField("last_name")]

    @property
    def name(self):
        return self.title

    @cached_property
    def is_active(self):
        return self.terms.filter(
            date_ended__isnull=True, position__isnull=False
        ).exists()

    def clean(self):
        super().clean()
        self.title = f"{self.first_name} {self.last_name}"

    def get_articles(self):
        return (
            ArticlePage.objects.live()
            .filter(authors__author=self.contributor)
            .order_by("-first_published_at")
            .all()
        )

    def get_positions_html(self):
        terms = self.current_terms
        builder = ""
        for i, term in enumerate(terms):
            if i == len(terms) - 1 and len(terms) > 1:
                builder += " and "

            position_prefix = ""
            if term.acting:
                if i == 0:
                    position_prefix += "Acting "
                else:
                    position_prefix += "acting "
            elif term.de_facto:
                if i == 0:
                    position_prefix += "<i>De facto</i> "
                else:
                    position_prefix += "<i>de facto</i> "

            builder += mark_safe(position_prefix) + term.position.title
            if i < len(terms) - 1 and len(terms) > 2:
                builder += ", "

        return mark_safe(builder)

    @cached_property
    def current_terms(self):
        return [term for term in self.terms.filter(date_ended__isnull=True)]

    @cached_property
    def get_active_positions(self):
        return [term.position for term in self.terms.all() if term.date_ended is None]

    @cached_property
    def get_previous_terms(self):
        return [term for term in self.terms.filter(date_ended__isnull=False)]

@register_snippet
class Position(models.Model):
    title = models.CharField(max_length=100)

    search_fields = [index.SearchField("title", partial_match=True)]

    autocomplete_search_field = "title"

    class Meta:
        ordering = ["title"]

    def autocomplete_label(self):
        return self.title

    @classmethod
    def autocomplete_create(kls: type, value: str):
        return kls.objects.create(title=value)

    def __str__(self):
        return self.title


@register_snippet
class Term(Orderable, models.Model):
    position = models.ForeignKey(
        Position, on_delete=models.PROTECT, related_name="terms"
    )
    person = ParentalKey(StaffPage, on_delete=models.SET_NULL, related_name="terms", null=True)
    date_started = models.DateField(blank=True, null=True)
    date_ended = models.DateField(blank=True, null=True)
    acting = models.BooleanField(default=False)
    de_facto = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.position.title} ({self.date_started}—{self.date_ended or "now"})'
