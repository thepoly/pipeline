from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register,
)

from .models import Subscription, Newsletter


class SubscriptionAdmin(ModelAdmin):
    model = Subscription
    menu_icon = "mail"


class NewsletterAdmin(ModelAdmin):
    model = Newsletter
    menu_icon = "doc-full"
    inspect_view_enabled = True
    inspect_template_name = "newsletter/inspect.html"


class NewsletterAdminGroup(ModelAdminGroup):
    items = (SubscriptionAdmin, NewsletterAdmin)
    menu_icon = "doc-full"


modeladmin_register(NewsletterAdminGroup)
