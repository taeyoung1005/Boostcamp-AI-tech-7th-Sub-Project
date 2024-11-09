from django.urls import path

from . import views

app_name = "classification"

urlpatterns = [
    path("classifcation", views.home, name="home"),
]
