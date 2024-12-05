# postline/models.py
from django.db import models
from wagtail.admin.panels import FieldPanel
from core.models import ArticlePage
from wagtail.models import Page

class PostlinePage(Page):
    """Page type for Instagram posts with generated images."""

    article = models.ForeignKey(
        ArticlePage,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='instagram_posts',
        help_text="The article this Instagram post is related to."
    )

    class Meta:
        verbose_name = "Instagram Post"
        verbose_name_plural = "Instagram Posts"