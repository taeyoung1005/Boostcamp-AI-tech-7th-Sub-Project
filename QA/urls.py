from django.urls import path
from . import views

app_name = "QA"

urlpatterns = [
    path("", views.question_list, name="question_list"),
    path("create/", views.create_question, name="create_question"),
    path("<int:question_id>/", views.question_detail, name="question_detail"),
    path("<int:question_id>/edit/", views.update_question, name="update_question"),
    path("<int:question_id>/delete/", views.delete_question, name="delete_question"),
    path("<int:question_id>/create_answer/", views.create_answer, name="create_answer"),
    path(
        "<int:question_id>/<int:answer_id>/edit/",
        views.update_answer,
        name="update_answer",
    ),
    path(
        "<int:question_id>/<int:answer_id>/delete/",
        views.delete_answer,
        name="delete_answer",
    ),
]
