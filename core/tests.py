from datetime import datetime, timedelta, timezone
from django.test import TestCase
from django.utils import timezone
from wagtail.core.models import Page, Site
from bs4 import BeautifulSoup
from wagtail.core.rich_text import RichText
import xml.etree.ElementTree as ET

from articles.models import ArticlePage, ArticlesIndexPage


class RecentArticlesFeedTest(TestCase):
    def setUp(self):
        home = Page.objects.get(slug="home")
        section_index = ArticlesIndexPage(title="Section", slug="section")
        home.add_child(instance=section_index)
        section_index.save_revision().publish()
        section_index.save()

        page = ArticlePage(
            headline="<p>Headline</p>",
            slug="article-page",
            title="Headline",
            live=False,
            body=[("paragraph", RichText("test body"))],
        )
        section_index.add_child(instance=page)
        section_index.save_revision().publish()
        section_index.save()
        page.save_revision()

    def test_empty_feed(self):
        resp = self.client.get("/feed/")
        root = ET.fromstring(resp.content)
        self.assertEqual(len(root[0].findall("item")), 0)

    def test_one_item(self):
        page = ArticlePage.objects.get()
        page.live = True
        page.go_live_at = datetime.now(timezone.utc)
        page.save_revision().publish()

        resp = self.client.get("/feed/")
        root = ET.fromstring(resp.content)
        item = root[0].find("item")
        self.assertIsNot(item, None)

        self.assertEqual(item.find("title").text, page.headline)
        self.assertEqual(item.find("description").text, str(page.body))
        self.assertEqual(item.find("link").text, page.full_url)
        self.assertEqual(
            item.find("pubDate").text,
            datetime.strftime(page.get_published_date(), "%a, %d %b %Y %H:%M:%S %z"),
        )
