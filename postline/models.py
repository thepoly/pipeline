from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
from django.db import models

class PostlinePage(Page):
    table_content = models.TextField(help_text="Enter the table content in CSV format or structured format")

    content_panels = Page.content_panels + [
        FieldPanel('table_content'),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        # This is an example of how you can generate table data. You can change it to your needs.
        context['table'] = [
            ['Header1', 'Header2', 'Header3'],
            ['Row1-Col1', 'Row1-Col2', 'Row1-Col3'],
            ['Row2-Col1', 'Row2-Col2', 'Row2-Col3'],
        ]
        return context