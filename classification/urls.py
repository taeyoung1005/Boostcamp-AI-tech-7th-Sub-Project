from django.urls import path

from . import views

app_name = "classification"

urlpatterns = [
    path("indroduction/", views.indroduction, name="introduction"),
    path("spaces/", views.spaces, name="spaces"),
]
