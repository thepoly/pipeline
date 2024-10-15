import calendar
from django.shortcuts import render
from django.utils import timezone

def index(request):
    current_year = timezone.now().year
    calendar_html = calendar.HTMLCalendar().formatyear(current_year)

    return render(request, 'postline/index.html', {
        'current_year': current_year,
        'calendar_html': calendar_html,
    })