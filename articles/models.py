import operator
from bs4 import BeautifulSoup
from django.core.paginator import Paginator
from django.db import models
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.blocks import RichTextBlock, ListBlock
from wagtail.admin.edit_handlers import (
    FieldPanel,
    StreamFieldPanel,
    MultiFieldPanel,
    InlinePanel,
    PageChooserPanel,
)
from wagtail.snippets.blocks import SnippetChooserBlock
from wagtail.snippets.models import register_snippet
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.search import index
from wagtailautocomplete.edit_handlers import AutocompletePanel
from modelcluster.fields import ParentalKey


class ArticlePage(Page):
    headline = RichTextField(features=["italic"])
    subdeck = RichTextField(features=["italic"], null=True, blank=True)
    kicker = models.ForeignKey(
        "articles.Kicker", null=True, blank=True, on_delete=models.PROTECT
    )
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
                AutocompletePanel("kicker", page_type="articles.Kicker"),
                InlinePanel("authors", label="Author", min_num=1),
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
            for i in range(min(5, len(found_articles))):
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


class ArticlesIndexPage(Page):
    subpage_types = ["ArticlePage"]

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


@register_snippet
class Kicker(models.Model):
    title = models.CharField(max_length=255)

    @classmethod
    def autocomplete_create(kls: type, value: str):
        return kls.objects.create(title=value)

    def __str__(self):
        return self.title


class ArticleAuthorRelationship(models.Model):
    article = ParentalKey(
        "ArticlePage", related_name="authors", on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        "core.StaffPage", related_name="articles", on_delete=models.PROTECT
    )

    panels = [PageChooserPanel("author")]

    class Meta:
        unique_together = ("article", "author")


class MigrationInformation(models.Model):
    """Contains information about articles migrated from WordPress posts at poly.rpi.edu."""

    article = models.OneToOneField(ArticlePage, on_delete=models.CASCADE)
    link = models.URLField(db_index=True)
    guid = models.CharField(max_length=255, primary_key=True)
