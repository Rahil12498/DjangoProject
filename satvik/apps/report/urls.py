from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
  path('get-report/', views.get_report, name='get_report'),
]