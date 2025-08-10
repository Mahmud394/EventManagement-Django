# core/urls.py
from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("no-permission/", views.no_permission, name="no_permission"),
    path("non-log/", views.non_log, name="non_log"),
    path("loged/", views.loged, name="loged"),
    path('', TemplateView.as_view(template_name='core/home.html'), name='home'),
]
