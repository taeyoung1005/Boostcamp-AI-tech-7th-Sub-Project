from django.urls import path
from . import views

app_name = "guestbook"

urlpatterns = [
    path("", views.comment_list, name="comment_list"),
]
