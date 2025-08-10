from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.http import JsonResponse
from django.contrib.auth.views import LoginView

from .forms import EventForm
from .models import Category, Event, RSVP


def event_list(request):
    qs = Event.objects.select_related('category')  # optimize category fetch

    q = request.GET.get('q')
    if q:
        qs = qs.filter(Q(name__icontains=q) | Q(location__icontains=q))

    cat = request.GET.get('category')
    if cat:
        qs = qs.filter(category__id=cat)

    start = request.GET.get('start_date')
    end = request.GET.get('end_date')
    if start and end:
        qs = qs.filter(date__range=[start, end])

    qs = qs.prefetch_related('rsvps__user').annotate(participant_count=Count('rsvps'))

    context = {
        "events": qs,
        "categories": Category.objects.all(),
    }
    return render(request, "events/event_list.html", context)


def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)

    user_is_organizer = False
    if request.user.is_authenticated:
        user_groups = request.user.groups.values_list('name', flat=True)
        user_is_organizer = 'organizer' in [g.lower() for g in user_groups] or request.user.is_superuser

    context = {
        'event': event,
        'user_is_organizer': user_is_organizer,
    }
    return render(request, 'events/event_detail.html', context)


@login_required
def event_create(request):
    if not request.user.groups.filter(name__in=['Organizer', 'Admin']).exists():
        return redirect('core:no_permission')

    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            ev = form.save(commit=False)
            ev.created_by = request.user
            ev.save()
            messages.success(request, "Event created successfully.")
            return redirect('events:event_detail', pk=ev.pk)
    else:
        form = EventForm()
    return render(request, "events/event_form.html", {"form": form})


@login_required
def event_update(request, pk):
    ev = get_object_or_404(Event, pk=pk)
    if not request.user.groups.filter(name__in=['Organizer', 'Admin']).exists():
        return redirect('core:no_permission')

    if request.method == "POST":
        form = EventForm(request.POST, request.FILES, instance=ev)
        if form.is_valid():
            form.save()
            messages.success(request, "Event updated successfully.")
            return redirect('events:event_detail', pk=ev.pk)
    else:
        form = EventForm(instance=ev)
    return render(request, "events/event_form.html", {"form": form, "event": ev})


@login_required
def event_delete(request, pk):
    ev = get_object_or_404(Event, pk=pk)
    if not request.user.groups.filter(name__in=['Organizer', 'Admin']).exists():
        return redirect('core:no_permission')

    if request.method == "POST":
        ev.delete()
        messages.success(request, "Event deleted successfully.")
        return redirect('events:event_list')
    return render(request, "events/event_confirm_delete.html", {"event": ev})


@login_required
def rsvp_event(request, pk):
    event = get_object_or_404(Event, pk=pk)

    # Only logged-in users can RSVP (enforced by @login_required)
    # Create RSVP or notify if already exists
    rsvp, created = RSVP.objects.get_or_create(user=request.user, event=event)
    if created:
        messages.success(request, "RSVP recorded. Confirmation email sent (if implemented).")
    else:
        messages.info(request, "You have already RSVP'd for this event.")
    return redirect('events:event_detail', pk=pk)


@login_required
def organizer_dashboard(request):
    if not request.user.groups.filter(name__in=['Organizer', 'Admin']).exists():
        return redirect('core:no_permission')

    today = timezone.localdate()
    all_events = Event.objects.select_related('category').prefetch_related('rsvps__user')

    total_events = all_events.count()
    total_participants = RSVP.objects.count()
    upcoming_events = all_events.filter(date__gt=today).count()
    past_events = all_events.filter(date__lt=today).count()
    todays_events = all_events.filter(date=today)

    context = {
        "total_events": total_events,
        "total_participants": total_participants,
        "upcoming_events": upcoming_events,
        "past_events": past_events,
        "todays_events": todays_events,
    }
    return render(request, "events/dashboard.html", context)


@login_required
def stats_endpoint(request):
    if not request.user.groups.filter(name__in=['Organizer', 'Admin']).exists():
        return JsonResponse({"error": "forbidden"}, status=403)

    today = timezone.localdate()
    t = request.GET.get('type', 'all')

    events = Event.objects.all()
    if t == 'upcoming':
        events = events.filter(date__gt=today)
    elif t == 'past':
        events = events.filter(date__lt=today)

    events = events.select_related('category').annotate(participant_count=Count('rsvps')).order_by('-date')[:20]

    data = [{
        "id": e.id,
        "name": e.name,
        "date": e.date.isoformat(),
        "participants": e.participant_count
    } for e in events]

    return JsonResponse({"events": data})


class RoleBasedLoginView(LoginView):
    template_name = 'users/login.html'

    def get_success_url(self):
        user = self.request.user
        if user.groups.filter(name='Admin').exists():
            return reverse_lazy('admin_dashboard')
        elif user.groups.filter(name='Organizer').exists():
            return reverse_lazy('organizer_dashboard')
        elif user.groups.filter(name='Participant').exists():
            return reverse_lazy('participant_dashboard')
        else:
            return reverse_lazy('core:home')
