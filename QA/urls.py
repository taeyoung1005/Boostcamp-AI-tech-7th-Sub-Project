from django.urls import path
from . import views

app_name = "QA"

urlpatterns = [
    path("", views.question_list, name="question_list"),
    path("<int:question_id>/", views.question_detail, name="question_detail"),
    path("create/", views.create_question, name="create_question"),
]
