from django.db import models
from wagtail.admin.panels import FieldPanel
from core.models import ArticlePage
from wagtail.models import Page

class PostlineIndexPage(ArticlePage):
    #Extension of ArticlePage that tracks Instagram posting status
    
    parent_page_types = ['core.ArticlesIndexPage']
    subpage_types = []

    posted = models.BooleanField(
        default=False,
        help_text="Whether this article has been posted to Instagram"
    )
    instagram_link = models.URLField(
        blank=True, 
        null=True,
        help_text="Link to the Instagram post"
    )

    def check_instagram_post(self):
        """Returns the Instagram link if posted, None otherwise"""
        if self.posted:
            return self.instagram_link
        return "Not Posted"

    content_panels = ArticlePage.content_panels + [
        FieldPanel('posted'),
        FieldPanel('instagram_link'),
    ]

    class Meta:
        verbose_name = "Extended Article Page"
        verbose_name_plural = "Extended Article Pages"

class PostlinePage(Page):
    """Page type for creating Instagram posts"""
    
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

    content_panels = Page.content_panels + [
        FieldPanel('article'),
        FieldPanel('posted'),
        FieldPanel('instagram_link'),
    ]

    class Meta:
        verbose_name = "Instagram Post"
        verbose_name_plural = "Instagram Posts"

