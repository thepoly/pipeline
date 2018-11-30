from django import template
from django.utils.safestring import mark_safe
from wagtail.core.rich_text import expand_db_html


register = template.Library()


@register.filter
def richtext_unwrapped(value):
    # if isinstance(value, RichText):
    #     return value
    if value is None:
        html = ""
    else:
        html = expand_db_html(value)

    if html.startswith("<p>") and html.endswith("</p>"):
        html = html[3:-4]
    return mark_safe(html)
