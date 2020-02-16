import datetime
from io import BytesIO
from os import path
import logging
import re
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
    ElectionIndexPage,
    NomCount,
    Office,
    NomCountOrderable,
    CandidatePage,
)


class Command(BaseCommand):
    help = "Imports articles from WordPress at poly.rpi.edu"

    def __init__(self):
        super().__init__()

        logging.getLogger("pipeline").setLevel(logging.WARN)

    def add_arguments(self, parser):
        parser.add_argument("election_id", type=int)

    def handle(self, *args, **options):
        self.election_id = options["election_id"]
        # get election page
        try:
            self.electionIndex = ElectionIndexPage.objects.get(
                electionID=self.election_id
            )
        except StaffIndexPage.DoesNotExist:
            self.stderr.write("Election index page does not exist in Pipeline.")
            exit(1)

        self.stdout.write(f"Importing election {self.election_id}")
        #  Import offices
        r = requests.get(
            "https://elections.union.rpi.edu/api/offices/election/"
            + str(self.election_id)
        )
        for office in r.json():
            try:
                Office.objects.get(
                    elections_site_id=office["office_id"],
                    election_in=office["election_id"],
                )
                print(f"Found office {office['name']}")
                continue
            except:
                print("Office Not Found, Creating")
                o = Office()
                o.name = office["name"]
                o.elections_site_id = office["office_id"]
                o.election_in = office["election_id"]
                o.save()

        # Import candidates
        r = requests.get("https://elections.union.rpi.edu/api/candidates")
        for candidate in r.json():
            pages = self.electionIndex.get_children().type(CandidatePage).all()
            pageFound = False
            for page in pages:
                if page.specific.rcs_id == candidate["rcs_id"]:
                    pageFound = True
                    office = Office.objects.get(
                        elections_site_id=candidate["office_id"],
                        election_in=candidate["election_id"],
                    )
                    print(f"scanning {candidate['rcs_id']} for {office.name}")
                    offices_set = [
                        r.office
                        for r in page.specific.nom_counts.select_related("office")
                    ]
                    officeFound = False
                    for o in offices_set:
                        if o.elections_site_id == int(candidate["office_id"]):
                            officeFound = True
                            continue
                    if officeFound:
                        continue
                    print(f"Office {office.name} not found, adding")
                    pageToUpdate = CandidatePage.objects.get(id=page.id)
                    nc = NomCountOrderable()
                    pageToUpdate.nom_counts = pageToUpdate.nom_counts.get_object_list() + [
                        nc
                    ]
                    nc.office = office
                    nc.count = 0
                    nc.required = 100
                    nc.page = pageToUpdate
                    nc.save()
                    pageToUpdate.save_revision()
                    print(f"Office {office.name} added to {candidate['rcs_id']}")
                    break
                    print(
                        f"Candidate with rcs id {candidate['rcs_id']} already exists, skipping"
                    )
            if not pageFound:
                page = CandidatePage()
                if (
                    candidate["preferred_name"] != None
                    and candidate["preferred_name"] != ""
                ):
                    page.title = (
                        f"{candidate['preferred_name']} {candidate['last_name']}"
                    )
                else:
                    page.title = f"{candidate['first_name']} {candidate['last_name']}"

                page.rcs_id = candidate["rcs_id"]
                page.election_site_id = -1
                page.live = False
                office = Office.objects.get(
                    elections_site_id=candidate["office_id"],
                    election_in=candidate["election_id"],
                )
                nc = NomCountOrderable()
                nc.office = office
                nc.count = 0
                nc.required = 100
                self.electionIndex.add_child(instance=page)
                nc.page = page
                nc.save()
                page.nom_counts = [nc]
                print(f"Added page for rcs id: {candidate['rcs_id']}")
                page.save_revision(submitted_for_moderation=True)
        print("updating nom counts")
        # Update noms
        r = requests.get("https://elections.union.rpi.edu/api/offices")
        office_json = r.json()
        pages = self.electionIndex.get_children().type(CandidatePage).all()
        for page in pages:
            for nc in page.specific.nom_counts.get_object_list():
                for office in office_json:
                    reqd = -1
                    pageToUpdate = CandidatePage.objects.get(id=page.id)
                    if nc.office.elections_site_id == office["office_id"]:
                        reqd = office["nominations_required"]
                        mnc = pageToUpdate.nom_counts.get(id=nc.id)
                        if reqd != -1:
                            mnc.required = reqd
                        mnc.save()
                        mnc.page = pageToUpdate

                        pageToUpdate.save_revision()

        r = requests.get("https://elections.union.rpi.edu/api/nominations/counts")

        for count in r.json():
            pages = self.electionIndex.get_children().type(CandidatePage).all()
            for page in pages:
                if page.specific.rcs_id == count["rcs_id"]:
                    for nc in page.specific.nom_counts.get_object_list():
                        if nc.office.elections_site_id == count["office_id"]:
                            reqd = -1
                            for office in office_json:
                                if count["office_id"] == office["office_id"]:
                                    reqd = office["nominations_required"]
                            pageToUpdate = CandidatePage.objects.get(id=page.id)
                            mnc = pageToUpdate.nom_counts.get(id=nc.id)
                            mnc.count = count["nominations"]
                            if reqd != -1:
                                mnc.required = reqd
                            mnc.save()
                            mnc.page = pageToUpdate
                            pageToUpdate.save_revision()
                            print(f"Updated noms for {pageToUpdate.rcs_id}")
