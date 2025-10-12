from django.urls import path
from . import views

urlpatterns = [
    path('',view=views.home, name='home'),
    path('status/', views.StatusView.as_view(), name='api-status'),
]
