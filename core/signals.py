from wagtail.core.signals import page_published, page_unpublished
from django.dispatch import receiver
from django.core.cache import cache
import logging

logger = logging.getLogger("pipeline")


@receiver([page_published, page_unpublished])
def page_changed_handler(sender, **kwargs):
    logger.info("Clearing cache due to page publish or unpublish")
    cache.clear()
