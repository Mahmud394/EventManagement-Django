# core/views.py
from django.shortcuts import render
from django.shortcuts import render
from events.models import Event
from django.utils import timezone

def home(request):
    today = timezone.now().date()
    upcoming_events = Event.objects.filter(date__gte=today).order_by('date')[:6]  # get next 6 upcoming events
    context = {
        'upcoming_events': upcoming_events,
    }
    return render(request, 'core/home.html', context)




def no_permission(request):
    return render(request, "core/no-permission.html")

def non_log(request):
    return render(request, "core/non-log.html")

def loged(request):
    return render(request, "core/loged.html")
