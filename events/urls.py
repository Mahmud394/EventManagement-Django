from django.urls import path
from events.views import (
    dashboard_view,
    event_list,
    event_detail,
    event_create,
    event_update,
    event_delete,
    participant_list,
    participant_create,
    participant_update,
    participant_delete,
    category_list,
    category_create,
    category_update,
    category_delete,
)

urlpatterns = [
    path('dashboard/', dashboard_view, name='dashboard'),

    path('list/', event_list, name='event-list'),
    path('create/', event_create, name='event-create'),
    path('detail/<int:pk>/', event_detail, name='event-detail'),
    path('update/<int:id>/', event_update, name='event-update'),
    path('delete/<int:id>/', event_delete, name='event-delete'),
    path('participants/', participant_list, name='participant-list'),
    path('participants/create/', participant_create, name='participant-create'),
    path('participants/update/<int:id>/', participant_update, name='participant-update'),
    path('participants/delete/<int:id>/', participant_delete, name='participant-delete'),
    path('categories/', category_list, name='category-list'),
    path('categories/create/', category_create, name='category-create'),
    path('categories/update/<int:id>/', category_update, name='category-update'),
    path('categories/delete/<int:id>/', category_delete, name='category-delete'),
]
