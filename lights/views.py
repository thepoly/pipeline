from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django.views.decorators.cache import never_cache

from .models import Color
from .forms import ColorForm


def index(request):
    return render(request, "lights/index.html")


@never_cache
def getColor(request):
    try:
        c = Color.objects.get(id=0)
    except Color.DoesNotExist:
        return HttpResponse("255\n0\n0", content_type="text/plain")
    return HttpResponse(c, content_type="text/plain")


def setColor(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    form = ColorForm(request.POST)
    if form.is_valid():
        try:
            c = Color.objects.get(id=0)
        except Color.DoesNotExist:
            c = Color()
        c.R = form.cleaned_data["R"]
        c.G = form.cleaned_data["G"]
        c.B = form.cleaned_data["B"]
        c.save()
        return HttpResponse()
    return HttpResponseBadRequest()
