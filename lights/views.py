from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Color


def index(request):
    template = loader.get_template("index.html")
    return HttpResponse(template.render({}, request))


def getColor(request):
    try:
        c = Color.objects.get(pk=0)
    except Color.DoesNotExist:
        return HttpResponse("255\n0\n0")
    return HttpResponse(c)
