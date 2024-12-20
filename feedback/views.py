from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.core.paginator import Paginator

from .models import Feedback
from .forms import FeedbackForm


@login_required(login_url="account:login")
def feedback_list(request):
    feedbacks = Feedback.objects.filter(is_deleted=False).order_by("-created_at")
    paginator = Paginator(feedbacks, 10)  # 페이지당 10개의 피드백 표시
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "feedback/feedback_list.html", {"page_obj": page_obj})


@login_required(login_url="account:login")
def create_feedback(request):
    """
    새로운 피드백을 작성하는 뷰입니다. 로그인한 사용자만 접근할 수 있습니다.
    """
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.author = request.user
            feedback.created_at = timezone.now()
            feedback.save()
            return redirect("feedback:feedback_list")
    else:
        form = FeedbackForm()
    return render(request, "feedback/create_feedback.html", {"form": form})


@login_required(login_url="account:login")
def feedback_detail(request, feedback_id):
    """
    피드백 상세 페이지를 보여주는 뷰입니다. 로그인한 사용자만 접근할 수 있습니다.
    """
    feedback = Feedback.objects.get(id=feedback_id)
    feedback.views_count += 1
    feedback.save(update_fields=["views_count"])
    return render(request, "feedback/feedback_detail.html", {"feedback": feedback})


@login_required(login_url="account:login")
def update_feedback(request, feedback_id):
    """
    피드백을 수정하는 뷰입니다. 로그인한 사용자만 접근할 수 있습니다.
    """
    feedback = get_object_or_404(Feedback, id=feedback_id, author=request.user)
    if request.method == "POST":
        form = FeedbackForm(request.POST, instance=feedback)
        if form.is_valid():
            form.save()
            messages.success(request, "Feedback updated successfully.")
            return redirect("feedback:feedback_detail", feedback_id=feedback.id)
    else:
        form = FeedbackForm(instance=feedback)
    return render(
        request, "feedback/update_feedback.html", {"form": form, "feedback": feedback}
    )


@login_required(login_url="account:login")
def delete_feedback(request, feedback_id):
    """
    피드백을 삭제하는 뷰입니다. 로그인한 사용자만 접근할 수 있습니다.
    """
    feedback = get_object_or_404(Feedback, id=feedback_id, author=request.user)
    if request.method == "POST":
        feedback.is_deleted = True
        feedback.save()
        messages.success(request, "Feedback deleted successfully.")
    return redirect("feedback:feedback_list")
