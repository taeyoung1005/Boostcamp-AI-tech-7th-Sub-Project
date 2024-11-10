# views.py

from django.shortcuts import render, get_object_or_404, redirect
from .models import Question, Answer
from .forms import QuestionForm, AnswerForm
from django.contrib.auth.decorators import login_required


def question_list(request):
    questions = Question.objects.all().order_by("-created_at")
    return render(request, "QA/question_list.html", {"questions": questions})


@login_required
def question_detail(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    answers = question.answers.all()
    question.views_count += 1
    question.save(update_fields=["views_count"])

    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.question = question
            answer.save()
            return redirect("QA:question_detail", question_id=question.id)
    else:
        form = AnswerForm()
    return render(
        request,
        "QA/question_detail.html",
        {"question": question, "answers": answers, "form": form},
    )


@login_required
def create_question(request):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.save()
            return redirect("QA:question_list")
    else:
        form = QuestionForm()
    return render(request, "QA/create_question.html", {"form": form})
