from django.urls import path
from . import views

app_name = "feedback"

urlpatterns = [
    path("", views.feedback_list, name="feedback_list"),
    path("create/", views.create_feedback, name="create_feedback"),
    path("<int:feedback_id>/", views.feedback_detail, name="feedback_detail"),
    path("<int:feedback_id>/edit/", views.update_feedback, name="update_feedback"),
    path("<int:feedback_id>/delete/", views.delete_feedback, name="delete_feedback"),
]
