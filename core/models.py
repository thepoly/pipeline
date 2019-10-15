import datetime
import logging
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
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.blocks import (
    RichTextBlock,
    ListBlock,
    StructBlock,
    URLBlock,
    StructValue,
    ChoiceBlock,
)
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page, Orderable
from wagtail.admin.edit_handlers import (
    FieldPanel,
    StreamFieldPanel,
    MultiFieldPanel,
    InlinePanel,
    PageChooserPanel,
)
from wagtail.embeds.embeds import get_embed
from wagtail.embeds.blocks import EmbedBlock
from wagtail.search import index
from wagtail.snippets.blocks import SnippetChooserBlock
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.models import Image, AbstractImage, AbstractRendition
from wagtailautocomplete.edit_handlers import AutocompletePanel
from modelcluster.fields import ParentalKey, ParentalManyToManyField


logger = logging.getLogger("pipeline")


class StaticPage(Page):
    body = RichTextField(blank=True, null=True)

    content_panels = Page.content_panels + [FieldPanel("body")]


@register_snippet
class Contributor(index.Indexed, models.Model):
    name = models.CharField(max_length=255)
    rich_name = RichTextField(
        features=["italic"], max_length=255, null=True, blank=True
    )

    search_fields = [index.SearchField("name", partial_match=True)]

    autocomplete_search_field = "name"

    def autocomplete_label(self):
        return self.name

    @classmethod
    def autocomplete_create(kls: type, value: str):
        return kls.objects.create(name=value)

    def get_articles(self):
        return [r.article for r in self.articles.select_related("article").all()]

    def __str__(self):
        return self.name


class StaffPage(Page):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    biography = RichTextField(null=True, blank=True)
    photo = models.ForeignKey(
        "CustomImage", null=True, blank=True, on_delete=models.PROTECT
    )
    email_address = models.EmailField(null=True, blank=True)
    contributor = models.OneToOneField(
        Contributor,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="staff_page",
    )

    content_panels = [
        MultiFieldPanel(
            [FieldPanel("first_name"), FieldPanel("last_name")], heading="Name"
        ),
        FieldPanel("email_address"),
        FieldPanel("biography"),
        ImageChooserPanel("photo"),
        InlinePanel("terms", label="Term", heading="Terms", min_num=0),
        SnippetChooserPanel("contributor"),
    ]

    search_fields = [index.SearchField("first_name"), index.SearchField("last_name")]

    parent_page_types = ["StaffIndexPage"]
    subpage_types = []

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


class StaffIndexPage(Page):
    subpage_types = ["StaffPage"]

    def get_active_staff(self):
        return (
            StaffPage.objects.live()
            .descendant_of(self)
            .filter(terms__position__isnull=False, terms__date_ended__isnull=True)
            .select_related("photo")
            .prefetch_related("terms__position")
            .distinct()
        )

    def get_previous_staff(self):
        return (
            StaffPage.objects.live()
            .descendant_of(self)
            .exclude(terms__date_ended__isnull=True, terms__position__isnull=False)
            .annotate(latest_term_ended=Max("terms__date_ended"))
            .order_by(F("latest_term_ended").desc(nulls_last=True))
        )


@register_snippet
class Position(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


@register_snippet
class Term(Orderable, models.Model):
    position = models.ForeignKey(
        Position, on_delete=models.PROTECT, related_name="terms"
    )
    person = ParentalKey(StaffPage, on_delete=models.PROTECT, related_name="terms")
    date_started = models.DateField(blank=True, null=True)
    date_ended = models.DateField(blank=True, null=True)
    acting = models.BooleanField(default=False)
    de_facto = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.position.title} ({self.date_started}—{self.date_ended or "now"})'


# https://docs.wagtail.io/en/v2.2.2/advanced_topics/images/custom_image_model.html
class CustomImage(AbstractImage):
    photographer = models.ForeignKey(
        Contributor,
        on_delete=models.CASCADE,
        related_name="images",
        blank=True,
        null=True,
    )

    admin_form_fields = Image.admin_form_fields + ("photographer",)

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


# Do feature detection when a user saves an image without a focal point
@receiver(pre_save, sender=CustomImage)
def image_feature_detection(sender, instance, **kwargs):
    # Make sure the image doesn't already have a focal point
    if not instance.has_focal_point():
        # Set the focal point
        instance.set_focal_point(instance.get_suggested_focal_point())


class CustomRendition(AbstractRendition):
    image = models.ForeignKey(
        CustomImage, on_delete=models.CASCADE, related_name="renditions"
    )

    class Meta:
        unique_together = ("image", "filter_spec", "focal_point_key")


# Delete the rendition image file when a rendition is deleted
# TODO: test if this actually works
@receiver(pre_delete, sender=CustomRendition)
def rendition_delete(sender, instance, **kwargs):
    instance.file.delete(False)


@register_snippet
class Kicker(models.Model):
    title = models.CharField(max_length=255)

    @classmethod
    def autocomplete_create(kls: type, value: str):
        return kls.objects.create(title=value)

    def __str__(self):
        return self.title


class EmbeddedMediaValue(StructValue):
    def type(self):
        embed_url = self.get("embed").url
        embed = get_embed(embed_url)
        return embed.type


class EmbeddedMediaBlock(StructBlock):
    embed = EmbedBlock(help_text="URL to the content to embed.")

    class Meta:
        value_class = EmbeddedMediaValue
        icon = "media"


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


class AdBlock(StructBlock):
    image = ImageChooserBlock(help_text="Image should be 22:7")
    link = URLBlock(label="target", required=False)

    class Meta:
        icon = "image"


class GalleryPhotoBlock(StructBlock):
    image = ImageChooserBlock()
    caption = RichTextBlock(features=["italic"], required=False)


class ArticlePage(RoutablePageMixin, Page):
    headline = RichTextField(features=["italic"])
    subdeck = RichTextField(features=["italic"], null=True, blank=True)
    kicker = models.ForeignKey(Kicker, null=True, blank=True, on_delete=models.PROTECT)
    body = StreamField(
        [
            ("paragraph", RichTextBlock()),
            ("photo", PhotoBlock()),
            ("photo_gallery", ListBlock(GalleryPhotoBlock(), icon="image")),
            ("embed", EmbeddedMediaBlock()),
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
        CustomImage,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        help_text="Shown at the top of the article and on the home page.",
    )
    featured_caption = RichTextField(features=["italic"], blank=True, null=True)

    content_panels = [
        MultiFieldPanel(
            [FieldPanel("headline", classname="title"), FieldPanel("subdeck")]
        ),
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
                ImageChooserPanel("featured_image"),
                FieldPanel("featured_caption"),
            ],
            heading="Metadata",
            classname="collapsible",
        ),
        FieldPanel("summary"),
        StreamFieldPanel("body"),
    ]

    search_fields = Page.search_fields + [
        index.SearchField("headline"),
        index.SearchField("subdeck"),
        index.SearchField("body"),
        index.SearchField("summary"),
        index.RelatedFields("kicker", [index.SearchField("title")]),
        index.SearchField("get_author_names", partial_match=True),
    ]

    subpage_types = []

    def clean(self):
        super().clean()

        soup = BeautifulSoup(self.headline, "html.parser")
        self.title = soup.text

    @route(r"^$")
    def post_404(self, request):
        """Return an HTTP 404 whenever the page is accessed directly.

        This is because it should instead by accessed by its date-based path,
        i.e. `<year>/<month>/<slug>/`."""
        raise Http404

    def set_url_path(self, parent):
        """Make sure the page knows its own path. The published date might not be set,
        so we have to take that into account and ignore it if so."""
        date = self.get_published_date() or timezone.now()
        self.url_path = f"{parent.url_path}{date.year}/{date.month:02d}/{self.slug}/"
        return self.url_path

    def serve_preview(self, request, mode_name):
        request.is_preview = True
        return self.serve(request)

    def get_context(self, request):
        context = super().get_context(request)
        context["authors"] = self.get_authors()
        return context

    def get_authors(self):
        return [r.author for r in self.authors.select_related("author")]

    def get_author_names(self):
        return [a.name for a in self.get_authors()]

    def get_published_date(self):
        return (
            self.go_live_at
            or self.first_published_at
            or getattr(self.get_latest_revision(), "created_at", None)
        )

    def get_text_html(self):
        """Get the HTML that represents paragraphs within the article as a string."""
        builder = ""
        for block in self.body:
            if block.block_type == "paragraph":
                builder += str(block.value)
        return builder

    def get_plain_text(self):
        builder = ""
        soup = BeautifulSoup(self.get_text_html(), "html.parser")
        for para in soup.findAll("p"):
            builder += para.text
            builder += " "
        return builder[:-1]

    def get_related_articles(self):
        found_articles = []
        related_articles = []
        current_article_text = self.get_plain_text()
        if current_article_text is not None:
            current_article_words = set(current_article_text.split(" "))
            authors = self.get_authors()
            for author in authors:
                articles = author.get_articles()
                for article in articles:
                    if article.headline != self.headline:
                        text_to_match = article.get_plain_text()
                        article_words = set(text_to_match.split(" "))
                        found_articles.append(
                            (
                                article,
                                len(
                                    list(
                                        current_article_words.intersection(
                                            article_words
                                        )
                                    )
                                ),
                            )
                        )
            found_articles.sort(key=operator.itemgetter(1), reverse=True)
            for i in range(min(4, len(found_articles))):
                related_articles.append(found_articles[i][0])
        return related_articles

    def get_first_chars(self, n=100):
        """Convert the body to HTML, extract the text, and then build
        a string out of it until we have at least n characters.
        If this isn't possible, then return None."""

        text = self.get_plain_text()
        if len(text) < n:
            return None

        punctuation = {".", "!"}
        for i in range(n, len(text)):
            if text[i] in punctuation:
                if i + 1 == len(text):
                    return text
                elif text[i + 1] == " ":
                    return text[: i + 1]

        return None

    def get_meta_tags(self):
        tags = {}
        tags["og:type"] = "article"
        tags["og:title"] = self.title
        tags["og:url"] = self.full_url
        tags["og:site_name"] = self.get_site().site_name

        # description: either the article's summary or first paragraph
        if self.summary is not None:
            soup = BeautifulSoup(self.summary, "html.parser")
            tags["og:description"] = soup.get_text()
            tags["twitter:description"] = soup.get_text()
        else:
            first_chars = self.get_first_chars()
            if first_chars is not None:
                tags["og:description"] = first_chars
                tags["twitter:description"] = first_chars

        # image
        if self.featured_image is not None:
            # pylint: disable=E1101
            rendition = self.featured_image.get_rendition("min-1200x1200")
            rendition_url = self.get_site().root_url + rendition.url
            tags["og:image"] = rendition_url
            tags["twitter:image"] = rendition_url

        tags["twitter:site"] = "@rpipoly"
        tags["twitter:title"] = self.title
        if "twitter:description" in tags and "twitter:image" in tags:
            tags["twitter:card"] = "summary_large_image"
        else:
            tags["twitter:card"] = "summary"

        return tags


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
            .select_related("kicker", "featured_image")
        )

    def get_context(self, request):
        context = super().get_context(request)
        paginator = Paginator(self.get_articles(), 24)
        page = request.GET.get("page")
        context["articles"] = paginator.get_page(page)
        return context


class ArticleAuthorRelationship(models.Model):
    article = ParentalKey(ArticlePage, related_name="authors", on_delete=models.CASCADE)
    author = models.ForeignKey(
        Contributor, related_name="articles", on_delete=models.PROTECT
    )

    panels = [SnippetChooserPanel("author")]

    class Meta:
        unique_together = [("article", "author")]


class ArchivesPage(RoutablePageMixin, Page):
    body = RichTextField(blank=True, null=True)
    content_panels = Page.content_panels + [FieldPanel("body")]
    subpage_types = []

    @route(r"(\d{4})/(\d{2})/$")
    def by_year_month(self, request, year, month, *args, **kwargs):
        articles = (
            ArticlePage.objects.filter(
                first_published_at__year=year, first_published_at__month=month
            )
            .order_by("-first_published_at")
            .select_related("kicker", "featured_image")
        )

        if len(articles) == 0:
            raise Http404

        date = datetime.datetime(int(year), int(month), 1)
        context = super().get_context(request)
        context["articles"] = articles
        context["date"] = date
        return render(request, "core/archives_page_list.html", context)

    def get_months(self):
        return ArticlePage.objects.live().dates("first_published_at", "month")


class MigrationInformation(models.Model):
    """Contains information about articles migrated from WordPress posts at poly.rpi.edu."""

    article = models.OneToOneField(ArticlePage, on_delete=models.CASCADE)
    link = models.URLField(db_index=True)
    guid = models.CharField(max_length=255, primary_key=True)
