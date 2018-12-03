from django.db import models

from wagtail.admin.edit_handlers import StreamFieldPanel, FieldPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.core import blocks
from wagtail.core.fields import StreamField

from articles.models import ArticlePage


class Subscription(models.Model):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email


class ArticleBlock(blocks.StructBlock):
    article = blocks.PageChooserBlock(target_model=ArticlePage)
    headline = blocks.RichTextBlock(
        help_text="Optional. Will override the article's headline.", required=False
    )
    summary = blocks.RichTextBlock(
        help_text="Optional. Will override the article's summary.", required=False
    )
    # TODO: add a photo override block
    # TODO: add a "hide photo" block

    # class Meta:
    #     template = "home/article_block.html"


class Newsletter(models.Model):
    subject = models.CharField(max_length=255)
    body = StreamField([("article", ArticleBlock()), ("text", blocks.RichTextBlock())])

    panels = [FieldPanel("subject"), StreamFieldPanel("body")]

    def get_html(self):
        return f"""<h1>{self.subject}</h1>{self.body}"""

    def __str__(self):
        return self.subject


@register_setting(icon="doc-full")
class NewsletterSettings(BaseSetting):
    subscriptions_token = models.CharField(
        max_length=255, help_text="The token required to access the subscription list"
    )

    class Meta:
        verbose_name = "newsletter settings"
