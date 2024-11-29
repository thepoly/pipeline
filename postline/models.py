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
    
    posted = models.BooleanField(
        default=False,
        help_text="Whether this post has been published to Instagram."
    )
    instagram_link = models.URLField(
        blank=True,
        null=True,
        help_text="Link to the Instagram post."
    )
    image = models.ImageField(
        upload_to='instagram_posts/',
        null=True,
        blank=True,
        help_text="Generated image for the Instagram post."
    )

    content_panels = Page.content_panels + [
        FieldPanel('article'),
        FieldPanel('posted'),
        FieldPanel('instagram_link'),
        FieldPanel('image'),
    ]

    class Meta:
        verbose_name = "Instagram Post"
        verbose_name_plural = "Instagram Posts"