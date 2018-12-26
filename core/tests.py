from datetime import datetime, timedelta, timezone
from django.test import TestCase
from django.utils import timezone
from wagtail.core.models import Page, Site
from bs4 import BeautifulSoup
from wagtail.core.rich_text import RichText
import xml.etree.ElementTree as ET

from .models import ArticlePage, ArticlesIndexPage


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

    def test_dump_cache_on_publish(self):
        page = ArticlePage.objects.get()
        page.headline = "Original headline"
        page.save_revision().publish()
        resp = self.client.get("/section/article-page/")
        self.assertContains(resp, "Original headline")
        self.assertNotContains(resp, "Updated headline")

        page = ArticlePage.objects.get()
        page.headline = "Updated headline"
        page.save_revision().publish()
        resp = self.client.get("/section/article-page/")
        self.assertNotContains(resp, "Original headline")
        self.assertContains(resp, "Updated headline")


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
        self.assertTemplateUsed(resp, "core/article_page.html")

    def test_title(self):
        resp = self.client.get("/section/article-page/")
        soup = BeautifulSoup(resp.content, "html.parser")
        self.assertEqual(soup.title.string.strip(), "Headline")

    def test_first_chars(self):
        test_body = """<p><span style="font-weight: 400;">Hi, RPI!</span></p>
<p><span style="font-weight: 400;">Today, I’d like to discuss a topic we’ve covered extensively in our MBA program, which I feel is applicable and pertinent to all group dynamics: handling conflict with constructive criticism.</span></p>
<p><span style="font-weight: 400;">A common sentiment I have heard, both from fellow students and in the workplace, is the desire to avoid conflict unless absolutely necessary. While maintaining harmony is valuable, sometimes conflict proves to be important for effective operation of groups. This, of course, includes our student groups, clubs, and organizations. One key difference that helps to ensure success lies in the framing and delivery of constructive criticism.</span></p>
<p><span style="font-weight: 400;">Earlier this semester, MBA students participating in the Design, Manufacturing, and Marketing course received an incredibly useful flyer, created by the Archer Center for Student Leadership, about delivering and receiving feedback effectively. Adapted from a book written by Harry Chambers, </span><i><span style="font-weight: 400;">Effective Communication Skills for Scientific and Technical Professionals,</span></i><span style="font-weight: 400;"> this flyer gives advice that I feel is valuable for the leaders of our clubs and organizations—Student Government included—and I have summarized the lessons I took from the flyer.</span></p>
<p><span style="font-weight: 400;">When delivering feedback, try to depersonalize the message by focusing on the behavior needing feedback, as opposed to the person behind the behavior. Also, work to ensure feedback is specific, actionable, factually based, and frequently given—and try to deliver this feedback privately. When given frequently and effectively, constructive criticism can prove vital to an organization’s ability to reflect, review, and revise course to increase the likelihood for success.</span></p>
<p><span style="font-weight: 400;">On the reverse, recipients of feedback should strive to keep an open mind and be willing to receive suggestions for improvement. Even if the criticism you have received is not constructive, try to explore the feedback for a deeper meaning. Furthermore, when receiving constructive criticism, do not be afraid to ask follow-up questions to help you better understand the issues at hand, and any possible solutions for moving forward.</span></p>
<p><span style="font-weight: 400;">Of course, we are not perfect, and mistakes happen on both sides—giving and receiving alike—but these ideals are worth striving towards. I have worked to adopt these lessons wherever I can, and I will continue to reflect on and revise my constructive criticism.</span></p>
<p><span style="font-weight: 400;">I hope groups find these suggestions useful! I believe these aspects of effectively giving and receiving feedback are essential to a healthy and successful team.</span></p>
<p><span style="font-weight: 400;">On a separate note, please remember that funded clubs must have a preliminary budget submitted via Club Management System by this Friday, November 16. These preliminary budgets can continue to be edited until the final submission deadline on November 26, but it is very important that a preliminary submission is made to help us ensure that clubs are on track for Fiscal Year 2020. Furthermore, no extensions can be granted to the November 26 final budget deadline, so please work with your Executive Board representative and student activities resource person, or SARP, to ensure your club’s budget is ready on time.</span></p>
<p><span style="font-weight: 400;">As always, if you have any questions, please do not hesitate to reach out to me at </span><a href="mailto:pu@rpi.edu"><span style="font-weight: 400;">pu@rpi.edu</span></a><span style="font-weight: 400;">!</span></p>"""
        a = ArticlePage()
        a.body = [("paragraph", RichText(test_body))]

        self.assertEqual(
            "Hi, RPI! Today, I’d like to discuss a topic we’ve covered extensively in our MBA program, which I feel is applicable and pertinent to all group dynamics: handling conflict with constructive criticism.",
            a.get_first_chars(20),
        )
        self.assertEqual("Hi, RPI!", a.get_first_chars(5))
