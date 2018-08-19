from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import PageChooserPanel, StreamFieldPanel
from wagtail.core import blocks


class ArticleBlock(blocks.StructBlock):
    article = blocks.PageChooserBlock(target_model="articles.ArticlePage")
    headline = blocks.RichTextBlock(
        help_text="Optional text to override the article headline", required=False
    )
    # TODO: add a photo override block

    class Meta:
        template = "home/article_block.html"


class OneColumnBlock(blocks.StructBlock):
    column = ArticleBlock()


class TwoColumnBlock(blocks.StructBlock):
    left_column = ArticleBlock()
    right_column = ArticleBlock()
    emphasize_column = blocks.ChoiceBlock(
        choices=[("left", "Left"), ("right", "Right")],
        required=False,
        help_text="Which article, if either, should appear larger.",
    )


class ThreeColumnBlock(blocks.StructBlock):
    left_column = ArticleBlock()
    middle_column = ArticleBlock()
    right_column = ArticleBlock()


class RecentArticlesBlock(blocks.StructBlock):
    num_articles = blocks.IntegerBlock()


class HomePage(Page):
    featured_articles = StreamField(
        [
            ("one_column", OneColumnBlock()),
            ("two_columns", TwoColumnBlock()),
            ("three_columns", ThreeColumnBlock()),
            ("recent_articles", RecentArticlesBlock()),
        ],
        null=True,
    )

    content_panels = Page.content_panels + [StreamFieldPanel("featured_articles")]
