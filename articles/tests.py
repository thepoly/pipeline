from datetime import datetime, timedelta
from django.test import TestCase
from django.utils import timezone
from wagtail.core.models import Page, Site
from bs4 import BeautifulSoup

from .models import ArticlePage, ArticlesIndexPage


class ArticlePageTest(TestCase):
    def setUp(self):
        home = Page.objects.get(slug="home")
        section_index = ArticlesIndexPage(title="Section", slug="section")
        home.add_child(instance=section_index)
        section_index.save_revision().publish()
        section_index.save()

        page = ArticlePage(
            headline="<p>Headline</p>", slug="article-page", title="Headline"
        )
        section_index.add_child(instance=page)
        section_index.save_revision().publish()
        section_index.save()
        page.save_revision().publish()

    def test_published_date(self):
        page = ArticlePage.objects.get()
        first_published = page.get_published_date()
        self.assertGreater(first_published, timezone.now() - timedelta(seconds=1))

        go_live = timezone.now()
        page.go_live_at = go_live
        page.save_revision().publish()
        self.assertEqual(page.get_published_date(), go_live)

        page.go_live_at = None
        page.save_revision().publish()
        self.assertEqual(page.get_published_date(), first_published)

    def test_status_code(self):
        resp = self.client.get("/section/article-page/")
        self.assertEqual(resp.status_code, 200)

    def test_template(self):
        resp = self.client.get("/section/article-page/")
        self.assertEqual(resp.template_name, "articles/article_page.html")

    def test_title(self):
        resp = self.client.get("/section/article-page/")
        soup = BeautifulSoup(resp.content, "html.parser")
        self.assertEqual(soup.title.string.strip(), "Headline")
