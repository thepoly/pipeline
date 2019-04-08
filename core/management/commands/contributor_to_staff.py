from io import BytesIO
from os import path
from urllib.parse import urlparse

from django.core.management.base import BaseCommand
from django.core.files.images import ImageFile
from django.db import transaction
from django.utils.text import slugify
from wagtail.core.rich_text import RichText
import requests
from requests.exceptions import RequestException

from core.models import StaffPage, StaffIndexPage, Contributor


class Command(BaseCommand):
    help = "Creates a staff page from a contributor."

    def __init__(self):
        super().__init__()
        # get staff page
        try:
            self.staff_index = StaffIndexPage.objects.get()
        except StaffIndexPage.DoesNotExist:
            self.stderr.write("Staff index page does not exist in Pipeline.")
            exit(1)

    def add_arguments(self, parser):
        parser.add_argument("contributor_name", type=str)

    def handle(self, *args, **options):
        self.stdout.write("Creating...")

        self.create(options["contributor_name"])

        self.stdout.write("Done.")

    @transaction.atomic
    def create(self, name):
        try:
            contributor = Contributor.objects.filter(name=name).get()
        except Contributor.DoesNotExist:
            self.stderr.write("Unable to find contributor with that name")
            exit(1)
        split = name.split(" ")
        staff_page = StaffPage()
        staff_page.first_name = split[0]
        staff_page.last_name = split[1]
        staff_page.title = f"{split[0]} {split[1]}"
        staff_page.slug = slugify(staff_page.title)
        self.staff_index.add_child(instance=staff_page)
        staff_page.save_revision().publish()
        contributor.staff_page = staff_page
        contributor.save()
