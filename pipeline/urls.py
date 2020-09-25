from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtailautocomplete.urls.admin import urlpatterns as autocomplete_admin_urls
from wagtail.contrib.sitemaps.views import sitemap

from search import views as search_views
from newsletter import urls as newsletter_urls
from core.feeds import RecentArticlesFeed
from lights import urls as lights_urls

from django.urls import path
from core.views import PostListView, PostDetailView

urlpatterns = [
    url(r"^lights/", include(lights_urls)),
    url(r"^django-admin/", admin.site.urls),
    url(r"^admin/autocomplete/", include(autocomplete_admin_urls)),
    url(r"^admin/", include(wagtailadmin_urls)),
    url(r"^documents/", include(wagtaildocs_urls)),
    url(r"^search/$", search_views.search, name="search"),
    url(r"^newsletter/", include(newsletter_urls), name="newsletter"),
    url(r"^feed/$", RecentArticlesFeed()),
    url(r"^sitemap\.xml$", sitemap),
]

urlpatterns += [
    url("", include("django_prometheus.urls")),
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    url(r"", include(wagtail_urls)),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    import debug_toolbar

    urlpatterns += [url(r"^__debug__/", include(debug_toolbar.urls))]


urlpatterns += [
    path('admin/', admin.site.urls),
    path('', PostListView.as_view(), name='posts'),
    path('<slug:slug>/', PostDetailView.as_view(), name='detail'),
    path('hitcount/', include(('hitcount.urls', 'hitcount'), namespace='hitcount')),
]
