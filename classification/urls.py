from django.urls import path

from . import views

app_name = "classification"

urlpatterns = [
    path("introduction/", views.introduction, name="introduction"),
    path("spaces/", views.spaces, name="spaces"),
]
