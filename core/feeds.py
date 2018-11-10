from django.contrib.syndication.views import Feed
from articles.models import ArticlePage


class RecentArticlesFeed(Feed):
    title = "The Polytechnic"
    link = "/"

    def items(self):
        return ArticlePage.objects.live().order_by("-first_published_at")[:20]

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
