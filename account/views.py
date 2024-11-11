from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm, UserUpdateForm
from main.models import Notification


def login(request):
    """
    사용자 로그인을 처리하는 뷰입니다.
    """
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        remember_me = request.POST.get("remember_me")

        # 사용자 인증
        user = authenticate(request, username=email, password=password)

        if user is not None:
            # 인증에 성공하면 로그인 처리
            auth_login(request, user)
            response = redirect("main:index")  # 로그인 성공 후 이동할 URL name
            # Remember Me 설정 처리
            if remember_me:
                # 쿠키에 이메일 저장 (1개월 동안 유지)
                response.set_cookie(
                    "remember_me_email", email, max_age=60 * 60 * 24 * 7
                )
            else:
                # Remember Me를 선택하지 않으면 쿠키 삭제
                response.delete_cookie("remember_me_email")
            return response
        else:
            # 인증 실패 시 오류 메시지
            messages.error(request, "Invalid email or password")

    remembered_email = request.COOKIES.get("remember_me_email", "")
    return render(request, "account/login.html", {"remembered_email": remembered_email})


def register(request):
    """
    사용자 등록을 처리하는 뷰입니다.
    """
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()  # 유효한 경우 사용자 저장
            messages.success(request, "Account created successfully. Please log in.")

            # 환영 알림 생성
            Notification.objects.create(
                user=user,
                title="Welcome to Our Platform!",
                message="Thank you for joining us! We hope you enjoy our services.",
                icon="success",  # 적절한 아이콘 선택 (예: success, info 등)
            )

            return redirect("account:login")  # 로그인 페이지로 리디렉션
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
    else:
        form = RegisterForm()

    return render(request, "account/register.html", {"form": form})


@login_required(login_url="account:login")
def logout(request):
    """
    사용자 로그아웃을 처리하는 뷰입니다.
    """

    # 로그아웃 처리
    auth_logout(request)

    return redirect("main:index")


@login_required(login_url="account:login")
def update_profile(request):
    """
    사용자 프로필을 업데이트하는 뷰입니다.
    """
    user = request.user

    if request.method == "POST":
        form = UserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully.")
            return redirect("account:update_profile")  # 프로필 페이지로 리디렉션
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = UserUpdateForm(instance=user)

    return render(request, "account/update_profile.html", {"form": form})
