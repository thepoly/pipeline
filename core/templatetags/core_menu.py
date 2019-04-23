from django import template

from core.models import ArticlesIndexPage
from home.models import HomePage

register = template.Library()


@register.simple_tag(takes_context=True)
def get_site_root(context):
    # NB this returns a core.Page, not the implementation-specific model used
    # so object-comparison to self will return false as objects would differ
    return context["request"].site.root_page


# Retrieves the top menu items - the immediate children of the parent page
# The has_menu_children method is necessary because the bootstrap menu requires
# a dropdown class to be applied to a parent
@register.inclusion_tag("core/tags/top_menu.html", takes_context=True)
def top_menu(context, parent, calling_page=None):
    divider_index = None
    menuitems = parent.get_children().live().in_menu()
    for i in range(len(menuitems)):
        menuitem = menuitems[i]
        # menuitem.show_dropdown = has_menu_children(menuitem)
        # We don't directly check if calling_page is None since the template
        # engine can pass an empty string to calling_page
        # if the variable passed as calling_page does not exist.
        menuitem.active = (
            calling_page.path.startswith(menuitem.path) if calling_page else False
        )

        # Add a divider after the links to sections and before the static pages.
        if (
            divider_index is None
            and len(menuitems) > 1
            and not isinstance(menuitem.specific, ArticlesIndexPage)
        ):
            divider_index = i - 1
    return {
        "calling_page": calling_page,
        "menuitems": menuitems,
        "divider_index": divider_index,
        "is_home": isinstance(calling_page, HomePage),
        # required by the pageurl tag that we want to use within this template
        "request": context["request"],
    }
