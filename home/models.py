from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.core import blocks

from core.models import ArticlePage, ArticlesIndexPage, AdBlock


class ArticleBlock(blocks.StructBlock):
    article = blocks.PageChooserBlock(target_model="core.ArticlePage")
    headline = blocks.RichTextBlock(
        help_text="Optional. Will override the article's headline.", required=False
    )
    # TODO: add a photo override block
    # TODO: add a "hide photo" block

    class Meta:
        template = "home/article_block.html"

class OneColumnBlock(blocks.StructBlock):
    column = ArticleBlock()

    def article_pks(self):
        return set(self.column.value.pk)  # pylint: disable=E1101

class OneColumnAdBlock(blocks.StructBlock):
    column = AdBlock()


class TwoColumnBlock(blocks.StructBlock):
    left_column = ArticleBlock()
    right_column = ArticleBlock()
    emphasize_column = blocks.ChoiceBlock(
        choices=[("left", "Left"), ("right", "Right")],
        required=False,
        help_text="Which article, if either, should appear larger.",
    )

    def article_pks(self):
        # pylint: disable=E1101
        return set(self.left_column.value.pk, self.right_column.value.pk)


class ThreeColumnBlock(blocks.StructBlock):
    left_column = ArticleBlock()
    middle_column = ArticleBlock()
    right_column = ArticleBlock()

    def article_pks(self):
        # pylint: disable=E1101
        return set(
            self.left_column.value.pk,
            self.middle_column.value.pk,
            self.right_column.value.pk,
        )


class RecentArticlesValue(blocks.StructValue):
    def get_articles(self):
        # Get the primary keys of all the articles manually placed on the homepage
        # so that we can exclude them here.
        homepage = HomePage.objects.get()
        pks = homepage.article_pks()
        return (
            a
            for a in ArticlePage.objects.live()
            .order_by("-first_published_at")
            .exclude(pk__in=pks)
            .prefetch_related("featured_image", "kicker")[: self["num_articles"]]
        )


class RecentArticlesBlock(blocks.StructBlock):
    num_articles = blocks.IntegerBlock(
        help_text="Number of recent articles to display.", label="Number of articles"
    )

    class Meta:
        value_class = RecentArticlesValue
        admin_text = (
            "Shows recent articles that are not manually placed elsewhere on the page."
        )


class HomePage(Page):
    featured_articles = StreamField(
        [
            ("one_column", OneColumnBlock()),
            ("one_ad_column", AdBlock()),
            ("two_columns", TwoColumnBlock()),
            ("three_columns", ThreeColumnBlock()),
            ("recent_articles", RecentArticlesBlock()),
        ],
        null=True,
    )

    content_panels = Page.content_panels + [StreamFieldPanel("featured_articles")]

    def article_pks(self):
        pks = set()
        for block in self.featured_articles:  # pylint: disable=E1133
            if block.block_type == "one_column":
                pks.add(block.value["column"]["article"].pk)
            elif block.block_type == "two_columns":
                pks.add(block.value["left_column"]["article"].pk)
                pks.add(block.value["right_column"]["article"].pk)
            elif block.block_type == "three_columns":
                pks.add(block.value["left_column"]["article"].pk)
                pks.add(block.value["middle_column"]["article"].pk)
                pks.add(block.value["right_column"]["article"].pk)
        return pks

    def get_sections(self):
        return list(ArticlesIndexPage.objects.live().descendant_of(self))
