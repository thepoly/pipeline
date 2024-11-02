from datetime import datetime, date

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.template.response import TemplateResponse
from django.shortcuts import render

from wagtail.models import Page
from wagtail.contrib.search_promotions.models import Query

from core.models import ArticlePage, ArticlesIndexPage

# To enable logging of search queries for use with the "Promoted search results" module
# <https://docs.wagtail.org/en/stable/reference/contrib/searchpromotions.html>
# uncomment the following line and the lines indicated in the search function
# (after adding wagtail.contrib.search_promotions to INSTALLED_APPS):

# from wagtail.contrib.search_promotions.models import Query


def search(request):
    search_query = request.GET.get("query", None)
    page = request.GET.get("page", 1)
    selected_section = request.GET.get("section", None)
    order = request.GET.get("order", None)
    start_date = request.GET.get("start_date", None)
    end_date = request.GET.get("end_date", None)

    sections = ArticlesIndexPage.objects.live().public()

    # Search
    if search_query:
        # filter based on order
        if order == "newest":
            search_results = ArticlePage.objects.live().public().order_by("-date").search(search_query)
        elif order == "oldest":
            search_results = ArticlePage.objects.live().public().order_by("date").search(search_query)
        else:
            search_results = ArticlePage.objects.live().public().search(search_query)

        # To log this query for use with the "Promoted search results" module:
        query = Query.get(search_query)
        query.add_hit()
    else:
        search_results = Page.objects.none()

    if selected_section:
        # search_results = search_results.filter(section=selected_section)

        # SQLite does not support filtering by related fields in search results, comment line below when using Postgres
        search_results = [result for result in search_results if result.get_parent().id == int(selected_section)]

    if start_date or end_date:
        if start_date:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        if end_date:
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()


        if start_date and end_date:
            # search_results = search_results.filter(date__range=[start_date, end_date])
            search_results = [result for result in search_results if start_date <= result.date <= end_date]
        elif start_date:
            # search_results = search_results.filter(date__gte=start_date)
            search_results = [result for result in search_results if result.date >= start_date]
        elif end_date:
            # search_results = search_results.filter(date__lte=end_date)
            search_results = [result for result in search_results if result.date <= end_date]

    # Pagination
    paginator = Paginator(search_results, 25)
    try:
        search_results = paginator.page(page)
    except PageNotAnInteger:
        search_results = paginator.page(1)
    except EmptyPage:
        search_results = paginator.page(paginator.num_pages)

    context = {
        "search_query": search_query,
        "search_results": search_results,
        "search_results_count": paginator.count,
        "selected_section": selected_section,
        "sections": sections,
        "order": order,
        "start_date": start_date,
        "end_date": end_date,
    }
    print(context)
    return render(request, "search/search.html", context)
