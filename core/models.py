from django.db import models

from wagtail.core.fields import RichTextField
from wagtail.core.models import Page, Orderable
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet
from wagtail.images.edit_handlers import ImageChooserPanel
from modelcluster.fields import ParentalKey


class StaticPage(Page):
    body = RichTextField()

    content_panels = Page.content_panels + [FieldPanel("body")]


class StaffPage(Page):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    biography = RichTextField(null=True, blank=True)
    photo = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True, on_delete=models.PROTECT
    )
    email_address = models.EmailField(null=True, blank=True)

    content_panels = [
        MultiFieldPanel(
            [FieldPanel("first_name"), FieldPanel("last_name")], heading="Name"
        ),
        FieldPanel("email_address"),
        FieldPanel("biography"),
        ImageChooserPanel("photo"),
        InlinePanel("terms", label="Term", heading="Terms"),
    ]

    search_fields = [index.SearchField("first_name"), index.SearchField("last_name")]

    parent_page_types = ["StaffIndexPage"]
    subpage_types = []

    def clean(self):
        super().clean()
        self.title = f"{self.first_name} {self.last_name}"

    def get_articles(self):
        return [r.article for r in self.articles.all()]

    def get_current_positions(self):
        return [
            t.position
            for t in self.terms.filter(date_ended__isnull=True).select_related(
                "position"
            )
        ]


class StaffIndexPage(Page):
    subpage_types = ["StaffPage"]

    def get_active_staff(self):
        return (
            StaffPage.objects.live()
            .descendant_of(self)
            .filter(terms__date_ended__isnull=True)
            .distinct()
        )


@register_snippet
class Position(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


@register_snippet
class Term(Orderable, models.Model):
    position = models.ForeignKey(
        Position, on_delete=models.PROTECT, related_name="terms"
    )
    person = ParentalKey(StaffPage, on_delete=models.PROTECT, related_name="terms")
    date_started = models.DateField()
    date_ended = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'{self.position.title} ({self.date_started}—{self.date_ended or "now"})'
