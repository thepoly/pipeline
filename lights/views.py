from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseBadRequest

from django.template import loader
from .models import Color
from .forms import ColorForm
from django.http import QueryDict


def index(request):
    template = loader.get_template("index.html")
    return HttpResponse(template.render({}, request))


def getColor(request):
    try:
        c = Color.objects.get(id=0)
    except Color.DoesNotExist:
        return HttpResponse("255\n0\n0")
    return HttpResponse(c)


def setColor(request):
    if request.method == "POST":
        form = ColorForm(request.POST)
        if form.is_valid():
            try:
                c = Color.objects.get(id=0)
                c.R = form.cleaned_data["R"]
                c.G = form.cleaned_data["G"]
                c.B = form.cleaned_data["B"]
                c.save()
                return HttpResponse()
            except Color.DoesNotExist:
                c = Color()
                c.R = form.cleaned_data["R"]
                c.G = form.cleaned_data["G"]
                c.B = form.cleaned_data["B"]
                c.save()
                return HttpResponse()
        else:
            return HttpResponseBadRequest()
