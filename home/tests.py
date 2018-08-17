from django.test import TestCase
from wagtail.core.models import Page, Site

from articles.models import ArticlePage
from .models import HomePage


class HomePageTest(TestCase):
    def setUp(self):
        default_home = Page.objects.get(title="Home")
        default_home.title = "Home Old"
        default_home.slug = "home-old"
        default_home.save_revision().publish()
        default_home.save()

        root_page = Page.get_root_nodes()[0]
        home_page = HomePage(title="Home", slug="home")
        root_page.add_child(instance=home_page)
        site = Site.objects.get()
        site.root_page = home_page
        site.save()
        default_home.delete()

    def test_featured_article(self):
        home_page = HomePage.objects.get(title="Home")
        page = ArticlePage(
            headline="<p>Headline</p>",
            slug="article-page",
            date="2018-08-17",
            title="Headline",
        )
        home_page.add_child(instance=page)
        home_page.save_revision().publish()
        home_page.save()
        page.save_revision().publish()
        page.save()

        home_page.featured_article = page
        home_page.save_revision().publish()
        home_page.save()

        resp = self.client.get("/")
        self.assertEqual(resp.context["page"].featured_article, page)

    def test_no_featured_article(self):
        resp = self.client.get("/")
        self.assertIsNone(resp.context["page"].featured_article)

    def test_status_code(self):
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)

    def test_template(self):
        resp = self.client.get("/")
        self.assertEqual(resp.template_name, "home/home_page.html")
