from django.db import models
import operator
from bs4 import BeautifulSoup

from wagtail.core.models import Page, PageManager
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.blocks import RichTextBlock
from wagtail.admin.edit_handlers import (
    FieldPanel,
    StreamFieldPanel,
    MultiFieldPanel,
    InlinePanel,
    PageChooserPanel,
)
from wagtail.snippets.models import register_snippet
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from modelcluster.fields import ParentalKey

from bs4 import BeautifulSoup


class ArticlePage(Page):
    headline = RichTextField(features=["italic"])
    subdeck = RichTextField(features=["italic"], null=True, blank=True)
    kicker = models.ForeignKey(
        "articles.Kicker", null=True, blank=True, on_delete=models.PROTECT
    )
    body = StreamField([("paragraph", RichTextBlock()), ("image", ImageChooserBlock())])
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
                # TODO: use https://github.com/wagtail/wagtail-autocomplete for kicker
                SnippetChooserPanel("kicker"),
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
            if block.block_type=="paragraph":
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
        found_articles=[]
        related_articles=[]
        current_article_text=self.get_text()
        current_article_words=set(current_article_text.split(" "))
        authors=self.get_authors()
        for author in authors:
            articles=author.get_articles()
            for article in articles:
                if article.headline!=self.headline:
                    text_to_match=article.get_text()
                    article_words=set(text_to_match.split(" "))
                    found_articles.append((article, len(list(current_article_words.intersection(article_words)))))
        found_articles.sort(key=operator.itemgetter(1), reverse=True)
        for i in range(5):
            related_articles.append(found_articles[i][0])
        return related_articles

class ArticlesIndexPage(Page):
    subpage_types = ["ArticlePage"]

    def get_articles(self):
        return ArticlePage.objects.live().descendant_of(self)


@register_snippet
class Kicker(models.Model):
    title = models.CharField(max_length=255)

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
