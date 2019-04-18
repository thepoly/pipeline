import logging
import operator

from bs4 import BeautifulSoup
from django.core.paginator import Paginator
from django.db import models
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from django.http import Http404
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.blocks import RichTextBlock, ListBlock
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page, Orderable
from wagtail.admin.edit_handlers import (
    FieldPanel,
    StreamFieldPanel,
    MultiFieldPanel,
    InlinePanel,
    PageChooserPanel,
)
from wagtail.search import index
from wagtail.snippets.blocks import SnippetChooserBlock
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.models import Image, AbstractImage, AbstractRendition
from wagtailautocomplete.edit_handlers import AutocompletePanel
from modelcluster.fields import ParentalKey


logger = logging.getLogger("pipeline")


class StaticPage(Page):
    body = RichTextField()

    content_panels = Page.content_panels + [FieldPanel("body")]


@register_snippet
class Contributor(models.Model):
    name = models.CharField(max_length=255, null=True)
    staff_page = models.OneToOneField("StaffPage", on_delete=models.PROTECT, null=True)

    def get_articles(self):
        return [r.article for r in self.articles.select_related("article").all()]

    def __str__(self):
        return self.name or self.staff_page.name


class StaffPage(Page):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    biography = RichTextField(null=True, blank=True)
    photo = models.ForeignKey(
        "CustomImage", null=True, blank=True, on_delete=models.PROTECT
    )
    email_address = models.EmailField(null=True, blank=True)

    content_panels = [
        MultiFieldPanel(
            [FieldPanel("first_name"), FieldPanel("last_name")], heading="Name"
        ),
        FieldPanel("email_address"),
        FieldPanel("biography"),
        ImageChooserPanel("photo"),
        InlinePanel("terms", label="Term", heading="Terms"),
    ]

    search_fields = [index.SearchField("first_name"), index.SearchField("last_name")]

    parent_page_types = ["StaffIndexPage"]
    subpage_types = []

    @property
    def name(self):
        return self.title

    def clean(self):
        super().clean()
        self.title = f"{self.first_name} {self.last_name}"

    def get_articles(self):
        return [
            r.article for r in self.contributor.articles.select_related("article").all()
        ]

    def get_current_positions(self):
        return [
            t.position
            for t in self.terms.filter(date_ended__isnull=True).select_related(
                "position"
            )
        ]

    def get_active_positions(self):
        return [term.position for term in self.terms.all() if term.date_ended is None]


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
    date_started = models.DateField()
    date_ended = models.DateField(blank=True, null=True)

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
class Photo(models.Model):
    image = models.ForeignKey(
        CustomImage, null=True, blank=True, on_delete=models.PROTECT
    )
    caption = RichTextField(blank=True, null=True)

    panels = [ImageChooserPanel("image"), FieldPanel("caption")]

    def __str__(self):
        return self.image.title


@register_snippet
class Kicker(models.Model):
    title = models.CharField(max_length=255)

    @classmethod
    def autocomplete_create(kls: type, value: str):
        return kls.objects.create(title=value)

    def __str__(self):
        return self.title


class ArticlePage(RoutablePageMixin, Page):
    headline = RichTextField(features=["italic"])
    subdeck = RichTextField(features=["italic"], null=True, blank=True)
    kicker = models.ForeignKey(Kicker, null=True, blank=True, on_delete=models.PROTECT)
    body = StreamField(
        [
            ("paragraph", RichTextBlock()),
            ("image", ImageChooserBlock()),
            ("photo_gallery", ListBlock(SnippetChooserBlock("core.Photo"))),
        ]
    )
    summary = RichTextField(
        features=["italic"],
        null=True,
        blank=True,
        help_text="Displayed on the home page or other places to provide a taste of what the article is about.",
    )
    featured_photo = models.ForeignKey(
        "core.Photo",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        help_text="Shown at the top of the article and on the home page.",
    )

    content_panels = [
        MultiFieldPanel(
            [FieldPanel("headline", classname="title"), FieldPanel("subdeck")]
        ),
        MultiFieldPanel(
            [
                AutocompletePanel("kicker", page_type="core.Kicker"),
                InlinePanel("authors", label="Author"),
                SnippetChooserPanel("featured_photo"),
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
        index.SearchField("get_author_names"),
    ]

    def clean(self):
        super().clean()

        soup = BeautifulSoup(self.headline, "html.parser")
        self.title = soup.text

    @route(r"^$")
    def post_404(self, request):
        """Return an HTTP 404 whenever the page is accessed directly.
        
        This is because it should instead by accessed by its date-based path,
        i.e. `<year>/<month>/<slug/`."""
        raise Http404

    def set_url_path(self, parent):
        """Make sure the page knows its own path. The published date might not be set,
        so we have to take that into account and ignore it if so."""
        date = self.first_published_at
        if date is not None:
            self.url_path = (
                f"{parent.url_path}{date.year}/{date.month:02d}/{self.slug}/"
            )
        else:
            self.url_path = f"{parent.url_path}{self.slug}/"
        return self.url_path

    def get_context(self, request):
        context = super().get_context(request)
        context["authors"] = self.get_authors()
        return context

    def get_authors(self):
        return [r.author for r in self.authors.select_related("author")]

    def get_author_names(self):
        return [f"{a.first_name} {a.last_name}" for a in self.get_authors()]

    def get_published_date(self):
        return self.go_live_at or self.first_published_at

    def get_text(self):
        builder = ""
        for block in self.body:
            if block.block_type == "paragraph":
                soup = BeautifulSoup(str(block.value), "html.parser")
                lines = soup.text.split("\n")
                first = True
                for line in lines:
                    if not first:
                        builder += " "
                        first = False
                    builder += line
                return builder

    def get_related_articles(self):
        found_articles = []
        related_articles = []
        current_article_text = self.get_text()
        if current_article_text is not None:
            current_article_words = set(current_article_text.split(" "))
            authors = self.get_authors()
            for author in authors:
                articles = author.get_articles()
                for article in articles:
                    if article.headline != self.headline:
                        text_to_match = article.get_text()
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

        builder = ""
        soup = BeautifulSoup(str(self.body), "html.parser")
        lines = soup.text.split("\n")
        for line in lines:
            builder += line + " "
            if len(builder) > n:
                return builder[:-1]
        return None

    def get_meta_tags(self):
        tags = {}
        tags["og:type"] = "article"
        tags["og:title"] = self.title
        tags["og:url"] = self.full_url
        tags["og:site_name"] = self.get_site().site_name

        # description: either the article's summary or first paragraph
        if self.summary is not None:
            tags["og:description"] = self.summary
            tags["twitter:description"] = self.summary
        else:
            first_paragraph = self.get_first_chars()
            if first_paragraph is not None:
                tags["og:description"] = first_paragraph
                tags["twitter:description"] = first_paragraph

        # image
        if self.featured_photo is not None:
            # pylint: disable=E1101
            rendition = self.featured_photo.image.get_rendition("fill-600x400")
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
            .order_by("-go_live_at")
            .select_related("featured_photo__image")
        )

    def get_context(self, request):
        context = super().get_context(request)
        paginator = Paginator(
            ArticlePage.objects.live()
            .descendant_of(self)
            .order_by("-go_live_at")
            .select_related("featured_photo__image"),
            24,
        )
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


class MigrationInformation(models.Model):
    """Contains information about articles migrated from WordPress posts at poly.rpi.edu."""

    article = models.OneToOneField(ArticlePage, on_delete=models.CASCADE)
    link = models.URLField(db_index=True)
    guid = models.CharField(max_length=255, primary_key=True)
