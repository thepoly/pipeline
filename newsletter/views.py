from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from django.views import View

from .forms import SubscriptionForm
from .models import Subscription, NewsletterSettings


class NewsletterView(View):
    def get(self, request):
        form = SubscriptionForm()
        return render(request, "newsletter/newsletter.html", {"form": form})

    def post(self, request):
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            return render(
                request,
                "newsletter/newsletter.html",
                {"message": "You are now subscribed."},
            )
        return render(request, "newsletter/newsletter.html", {"form": form})


class SubscriptionsView(View):
    def get(self, request):
        settings = NewsletterSettings.for_site(request.site)
        if request.GET.get("token") != settings.subscriptions_token:
            return HttpResponseForbidden()
        subscriptions = Subscription.objects.all()
        emails = (s.email for s in subscriptions)
        return HttpResponse("\n".join(emails), content_type="text/plain")
