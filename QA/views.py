# views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator

from .models import Question, Answer
from .forms import QuestionForm, AnswerForm


@login_required(login_url="account:login")
def question_list(request):
    """
    질문 목록을 보여주는 뷰입니다. 로그인한 사용자만 접근할 수 있습니다.
    """
    questions = Question.objects.filter(is_deleted=False).order_by("-created_at")
    paginator = Paginator(questions, 10)  # 페이지당 10개의 질문 표시
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)  # 현재 페이지 객체 가져오기

    return render(request, "QA/question_list.html", {"page_obj": page_obj})


@login_required(login_url="account:login")
def question_detail(request, question_id):
    """
    질문 상세 페이지를 보여주는 뷰입니다. 로그인한 사용자만 접근할 수 있습니다.
    """
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
    """
    새로운 질문을 작성하는 뷰입니다. 로그인한 사용자만 접근할 수 있습니다.
    """
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
    """
    질문을 수정하는 뷰입니다. 로그인한 사용자만 접근할 수 있습니다.
    """
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
    """
    질문을 삭제하는 뷰입니다. 로그인한 사용자만 접근할 수 있습니다.
    """
    question = get_object_or_404(Question, id=question_id, author=request.user)
    if request.method == "POST":
        question.is_deleted = True
        question.save()
        messages.success(request, "Question deleted successfully.")
    return redirect("QA:question_list")


@login_required(login_url="account:login")
def create_answer(request, question_id):
    """
    질문에 답변을 작성하는 뷰입니다. 로그인한 사용자만 접근할 수 있습니다.
    """
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
    """
    답변을 수정하는 뷰입니다. 로그인한 사용자만 접근할 수 있습니다.
    """
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
    """
    답변을 삭제하는 뷰입니다. 로그인한 사용자만 접근할 수 있습니다.
    """
    answer = get_object_or_404(
        Answer, id=answer_id, question_id=question_id, author=request.user
    )
    if request.method == "POST":
        answer.is_deleted = True
        answer.save()
        messages.success(request, "Answer deleted successfully.")
    return redirect("QA:question_detail", question_id=question_id)
