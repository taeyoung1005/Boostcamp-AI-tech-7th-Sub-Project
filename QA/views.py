# views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Question, Answer
from .forms import QuestionForm, AnswerForm


@login_required(login_url="account:login")
def question_list(request):
    questions = Question.objects.filter(is_deleted=False).order_by("-created_at")
    return render(request, "QA/question_list.html", {"questions": questions})


@login_required(login_url="account:login")
def question_detail(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    answers = question.answers.filter(is_deleted=False).order_by("-created_at")
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


@login_required(login_url="account:login")
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


@login_required(login_url="account:login")
def update_question(request, question_id):
    question = get_object_or_404(Question, id=question_id, author=request.user)
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save()
            messages.success(request, "Question updated successfully.")
            return redirect("QA:question_detail", question_id=question.id)
    else:
        form = QuestionForm(instance=question)
    return render(
        request, "QA/update_question.html", {"form": form, "question": question}
    )


@login_required(login_url="account:login")
def delete_question(request, question_id):
    question = get_object_or_404(Question, id=question_id, author=request.user)
    if request.method == "POST":
        question.is_deleted = True
        question.save()
        messages.success(request, "Question deleted successfully.")
    return redirect("QA:question_list")


@login_required(login_url="account:login")
def create_answer(request, question_id):
    question = get_object_or_404(Question, id=question_id)
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
        request, "QA/create_answer.html", {"form": form, "question": question}
    )


@login_required(login_url="account:login")
def update_answer(request, question_id, answer_id):
    answer = get_object_or_404(Answer, id=answer_id, question_id=question_id)
    if request.user != answer.author:
        return redirect("QA:question_list")

    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save()
            messages.success(request, "Answer updated successfully.")
            return redirect("QA:question_detail", question_id=question_id)
    else:
        form = AnswerForm(instance=answer)
    return render(
        request,
        "QA/update_answer.html",
        {"form": form, "answer": answer, "question_id": question_id},
    )


@login_required(login_url="account:login")
def delete_answer(request, question_id, answer_id):
    answer = get_object_or_404(
        Answer, id=answer_id, question_id=question_id, author=request.user
    )
    if request.method == "POST":
        answer.is_deleted = True
        answer.save()
        messages.success(request, "Answer deleted successfully.")
    return redirect("QA:question_detail", question_id=question_id)
