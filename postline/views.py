import calendar
from django.shortcuts import render
from django.utils import timezone

from core.models import ArticlePage

def index(request):
    current_year = timezone.now().year
    calendar_html = calendar.HTMLCalendar().formatyear(current_year)

    return render(request, 'postline/index.html', {
        'current_year': current_year,
        'calendar_html': calendar_html,
    })

def display_table(request):
    # Sample data for the table
    data = [
        {'name': 'Alice', 'age': 30, 'city': 'New York'},
        {'name': 'Bob', 'age': 25, 'city': 'Los Angeles'},
        {'name': 'Charlie', 'age': 35, 'city': 'Chicago'},
    ]
    return render(request, 'postline/table.html', {'data': data})

def display_articles_table(request):
    # Fetch all articles
    articles = ArticlePage.objects.live().order_by('-date')
    return render(request, 'postline/table.html', {'articles': articles})