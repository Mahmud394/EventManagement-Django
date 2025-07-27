from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import now
from django.db.models import Count, Q
from .models import Event, Participant, Category
from .forms import EventForm, ParticipantForm, CategoryForm

def dashboard_view(request):
    today = now().date()
    total_events = Event.objects.count()
    total_participants = Participant.objects.count()
    upcoming_events = Event.objects.filter(date__gt=today).count()
    past_events = Event.objects.filter(date__lt=today).count()
    today_events = Event.objects.filter(date=today).select_related('category').prefetch_related('participants')

    context = {
        'total_events': total_events,
        'total_participants': total_participants,
        'upcoming_events': upcoming_events,
        'past_events': past_events,
        'today_events': today_events,
        'events': Event.objects.all()[:6],  
    }
    return render(request, 'dashboard.html', context)


# Event Views 
def event_list(request):
    queryset = Event.objects.select_related('category').prefetch_related('participants').all()
    query = request.GET.get('q')
    category_filter = request.GET.get('category')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if query:
        queryset = queryset.filter(Q(name__icontains=query) | Q(location__icontains=query))
    if category_filter:
        queryset = queryset.filter(category__id=category_filter)
    if start_date and end_date:
        queryset = queryset.filter(date__range=[start_date, end_date])

    categories = Category.objects.all()
    context = {'events': queryset, 'categories': categories}
    return render(request, 'event_list.html', context)


def event_detail(request, pk):
    event = get_object_or_404(Event.objects.select_related('category').prefetch_related('participants'), pk=pk)
    return render(request, 'event_detail.html', {'event': event})


def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save()
            return redirect('event-detail', id=event.pk) 
    else:
        form = EventForm()
    return render(request, 'event_form.html', {'form': form})



def event_update(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event-detail', pk=pk)
    else:
        form = EventForm(instance=event)
    return render(request, 'event_form.html', {'form': form})


def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.delete()
        return redirect('event-list')
    return render(request, 'event_confirm_delete.html', {'event': event})


#  Participant Views

def participant_list(request):
    participants = Participant.objects.prefetch_related('events').all()
    return render(request, 'participant_list.html', {'participants': participants})


def participant_create(request):
    if request.method == 'POST':
        form = ParticipantForm(request.POST)
        if form.is_valid():
            participant = form.save()
            return redirect('participant-list')
    else:
        form = ParticipantForm()
    return render(request, 'participant_form.html', {'form': form})


def participant_update(request, pk):
    participant = get_object_or_404(Participant, pk=pk)
    if request.method == 'POST':
        form = ParticipantForm(request.POST, instance=participant)
        if form.is_valid():
            form.save()
            return redirect('participant-list')
    else:
        form = ParticipantForm(instance=participant)
    return render(request, 'participant_form.html', {'form': form})


def participant_delete(request, pk):
    participant = get_object_or_404(Participant, pk=pk)
    if request.method == 'POST':
        participant.delete()
        return redirect('participant-list')
    return render(request, 'participant_confirm_delete.html', {'participant': participant})


#  Category Views 

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})


def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category-list')
    else:
        form = CategoryForm()
    return render(request, 'category_form.html', {'form': form})


def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category-list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'category_form.html', {'form': form})


def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('category-list')
    return render(request, 'category_confirm_delete.html', {'category': category})
