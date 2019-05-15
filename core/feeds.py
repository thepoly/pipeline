from django.contrib.syndication.views import Feed
from core.models import ArticlePage, ArticlesIndexPage


class RecentArticlesFeed(Feed):
    title = "The Polytechnic"
    link = "/"
    description = "The RSS feed for all of the articles published by The Polytechnic, RPI's student newspaper"

    def items(self):
        return ArticlePage.objects.live().order_by("-first_published_at")[:40]

    def item_title(self, item):
        return item.headline

    def item_description(self, item):
        return item.body

    def item_link(self, item):
        return item.full_url

    def item_author_name(self, item):
        authors = item.get_author_names()
        return ", ".join(authors)

    def item_pubdate(self, item):
        return item.get_published_date()

class NewsArticlesFeed(Feed):
    def get_object(self, request, section):
        return ArticlesIndexPage.objects.get(slug=section)

    def title(self, obj):
        return "The Polytechnic's {} feed".format(obj.slug)

    link = "/"

    def description(self, obj):
        return "The RSS feed for all of the {} articles published by The Polytechnic, RPI's student newspaper".format(obj.slug)

    def items(self, obj):
        return ArticlePage.objects.live().child_of(obj).order_by("-first_published_at")[:20]

    def item_title(self, item):
        return item.headline

    def item_description(self, item):
        return item.body

    def item_link(self, item):
        return item.full_url

    def item_author_name(self, item):
        authors = item.get_author_names()
        return ", ".join(authors)

    def item_pubdate(self, item):
        return item.get_published_date()