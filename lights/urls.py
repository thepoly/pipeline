from django.urls import path
from django.contrib import admin

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("LEDP.txt", views.getColor, name="get color"),
    path("submit", views.setColor, name="set color"),
]
