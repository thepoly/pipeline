from django.shortcuts import redirect

from core.models import MigrationInformation


class MigrationRedirectMiddleware:
    """Attempt to redirect from migrated WordPress URLs to new Pipeline URLs on 404."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == 404:
            try:
                migration_info = MigrationInformation.objects.get(link=request.path)
            except MigrationInformation.DoesNotExist:
                return response

            return redirect(migration_info.article.url)

        return response
