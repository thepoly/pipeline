from io import BytesIO
from os import path
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from django.core.files.images import ImageFile
from django.db import transaction
from django.utils.text import slugify
from wagtail.core.rich_text import RichText
import requests
from requests.exceptions import RequestException

from core.models import (
    ArticlePage,
    ArticlesIndexPage,
    ArticleAuthorRelationship,
    Kicker,
    MigrationInformation,
    StaffPage,
    StaffIndexPage,
    CustomImage,
    Contributor,
)


class Command(BaseCommand):
    help = "Imports articles from WordPress at poly.rpi.edu"

    def __init__(self):
        super().__init__()
        # get staff page
        try:
            self.staff_index = StaffIndexPage.objects.get()
        except StaffIndexPage.DoesNotExist:
            self.stderr.write("Staff index page does not exist in Pipeline.")
            exit(1)

    def handle(self, *args, **options):
        self.stdout.write("Importing...")

        self.wp_import("Opinion", 3)
        self.wp_import("News", 5)
        self.wp_import("Features", 4)

        self.stdout.write("Done.")

    @transaction.atomic
    def wp_import(self, section_name, wp_category_id):
        try:
            section = ArticlesIndexPage.objects.get(title=section_name)
        except ArticlesIndexPage.DoesNotExist:
            self.stderr.write(f"{section_name} section does not exist in Pipeline.")
            exit(1)

        r = requests.get(
            "https://poly.rpi.edu/wp-json/wp/v2/posts?per_page=50",
            {"categories": wp_category_id},
        )
        j = r.json()
        for post in j:
            if not self.can_import(post):
                title = post["title"]["rendered"]
                self.stdout.write(f'Skipping "{title}"')
                continue

            self.stdout.write(self.style.SUCCESS(post["title"]["rendered"]))

            if ArticlePage.objects.filter(slug=post["slug"]).count():
                article = ArticlePage.objects.get(slug=post["slug"])
                self.update_article(article, post)
            else:
                self.create_article(section, post)

        section.save_revision().publish()

    def can_import(self, post):
        author_name = post["meta"]["AuthorName"]
        if ", " in author_name in author_name:
            return False

        return True

    def create_article(self, section, post):
        article = ArticlePage()
        article.slug = post["slug"]
        article.title = post["title"]["rendered"]
        article.headline = post["title"]["rendered"]
        section.add_child(instance=article)
        self.update_article(article, post)

    def update_article(self, article, post):
        article.subdeck = post["meta"]["Subdeck"]
        article.body = [("paragraph", RichText(post["content"]["rendered"]))]
        article.go_live_at = post["date"] + "Z"
        article.first_published_at = post["date"] + "Z"

        for author in self.create_or_get_authors(post["meta"]["AuthorName"]):
            try:
                rel = ArticleAuthorRelationship.objects.get(
                    article=article, author=author
                )
            except ArticleAuthorRelationship.DoesNotExist:
                rel = ArticleAuthorRelationship(article=article, author=author)
                article.save()
                rel.save()

        kicker = self.create_or_get_kicker(post["meta"]["Kicker"])
        article.kicker = kicker

        if post["meta"]["Photo"]:
            self.attach_featured_photo(
                article,
                post["meta"]["Photo"],
                post["meta"]["PhotoCaption"],
                post["meta"]["PhotoByline"],
            )

        article.save_revision().publish()

        guid = post["guid"]["rendered"]
        try:
            migration_info = MigrationInformation.objects.get(guid=guid)
        except MigrationInformation.DoesNotExist:
            migration_info = MigrationInformation(guid=guid)
        migration_info.article = article
        migration_info.link = post["link"][len("https://poly.rpi.edu") :]
        migration_info.save()

    def create_or_get_authors(self, authors):
        author_objects = []
        for author in authors.split(" and "):
            # splitted = author.split(" ")
            # if len(splitted) != 2:
            #     print(splitted)
            #     return author_objects
            # first_name = splitted[0]
            # last_name = splitted[1]

            soup = BeautifulSoup(author, "html.parser")
            name = soup.text

            try:
                contributor = Contributor.objects.filter(name=name).get()
            except Contributor.DoesNotExist:
                # staff_page = StaffPage()
                # staff_page.first_name = first_name
                # staff_page.last_name = last_name
                # staff_page.title = f"{first_name} {last_name}"
                # staff_page.slug = slugify(staff_page.title)
                # self.staff_index.add_child(instance=staff_page)
                # staff_page.save_revision().publish()
                contributor = Contributor(name=name, rich_name=author)
                contributor.save()
            author_objects.append(contributor)
        return author_objects

    def create_or_get_author(self, author):
        authors = self.create_or_get_authors(author)
        if len(authors) != 1:
            self.stderr.write(f"{author} could not be added as photographer.")
            return None
        return authors[0]

    def create_or_get_kicker(self, kicker_text):
        normalized = kicker_text.title()
        try:
            kicker = Kicker.objects.filter(title=normalized).get()
        except Kicker.DoesNotExist:
            kicker = Kicker()
            kicker.title = normalized
            kicker.save()
        return kicker

    def attach_featured_photo(self, article, photo_url, caption, photographer):
        if not photo_url.startswith("https://poly.rpi.edu"):
            photo_url = "https://poly.rpi.edu" + photo_url

        req = requests.Request("GET", photo_url)
        prepared = req.prepare()

        name = path.basename(urlparse(prepared.url).path)
        if article.featured_image and article.featured_image.title == name:
            # already grabbed this one
            return

        s = requests.Session()
        try:
            r = s.send(prepared)
        except RequestException as e:
            self.stderr.write(f"Unable to get photo from URL '{photo_url}'.")
            raise (e)

        image = CustomImage(file=ImageFile(BytesIO(r.content), name=name), title=name)
        if not photographer.startswith("Courtesy of "):
            photographer_name = photographer.split("/")[0]
            contributor = self.create_or_get_author(photographer_name)
            image.photographer = contributor
        image.save()

        article.featured_image = image
        article.featured_caption = RichText(caption)
