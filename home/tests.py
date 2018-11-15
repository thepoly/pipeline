from django.test import TestCase
from wagtail.core.models import Page, Site
from bs4 import BeautifulSoup

from articles.models import ArticlePage
from .models import HomePage


class HomePageTest(TestCase):
    def setUp(self):
        default_home = Page.objects.get(slug="home")
        default_home.title = "Home Old"
        default_home.slug = "home-old"
        default_home.save_revision().publish()
        default_home.save()

        root_page = Page.get_root_nodes()[0]
        home_page = HomePage(title="Home", slug="home")
        root_page.add_child(instance=home_page)
        site = Site.objects.get()
        site.root_page = home_page
        site.site_name = "The Polytechnic"
        site.save()
        default_home.delete()

    def test_featured_article(self):
        home_page = HomePage.objects.get(title="Home")
        page = ArticlePage(
            headline="<p>Headline</p>", slug="article-page", title="Headline"
        )
        home_page.add_child(instance=page)
        home_page.save_revision().publish()
        home_page.save()
        page.save_revision().publish()
        page.save()

        featured_articles = [
            (b.block_type, b.value) for b in home_page.featured_articles
        ]
        featured_articles.append(("one_column", {"column": {"article": page}}))
        home_page.featured_articles = featured_articles
        home_page.save_revision().publish()
        home_page.save()

        resp = self.client.get("/")
        blocks = resp.context["page"].featured_articles
        self.assertEqual(len(blocks), 1)

    def test_no_featured_article(self):
        resp = self.client.get("/")
        self.assertEqual(len(resp.context["page"].featured_articles), 0)

    def test_status_code(self):
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)

    def test_template(self):
        resp = self.client.get("/")
        self.assertTemplateUsed(resp, "home/home_page.html")

    def test_title(self):
        resp = self.client.get("/")
        soup = BeautifulSoup(resp.content, "html.parser")
        self.assertEqual(soup.title.string.strip(), "The Polytechnic")
