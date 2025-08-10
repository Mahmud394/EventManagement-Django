# events/urls.py
from django.urls import path,include
from . import views

app_name = "events"

urlpatterns = [
    path("", views.event_list, name="event_list"),
    path("create/", views.event_create, name="event_create"),
    path("<int:pk>/", views.event_detail, name="event_detail"),
    path("<int:pk>/update/", views.event_update, name="event_update"),
    path("<int:pk>/delete/", views.event_delete, name="event_delete"),
    path("<int:pk>/rsvp/", views.rsvp_event, name="rsvp_event"),
    path("dashboard/", views.organizer_dashboard, name="dashboard"),
    path("api/stats/", views.stats_endpoint, name="stats_endpoint"),
    path('', include('core.urls')),
    path('<int:pk>/rsvp/', views.rsvp_event, name='rsvp_event'),
]
