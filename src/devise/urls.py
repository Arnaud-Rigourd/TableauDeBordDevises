from django.urls import path

from .views import dashboard, redirect_index

urlpatterns = [
    path("", redirect_index, name="devise-index"),
    path("days=<int:days_range>&currencies=<str:chosen_currencies>", dashboard, name="devise-dashboard")
]