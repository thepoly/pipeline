from django.urls import path
from django.contrib import admin

from . import views

urlpatterns = [
    path("", views.NewsletterView.as_view(), name="newsletter"),
    path("subscriptions", views.SubscriptionsView.as_view()),
]
