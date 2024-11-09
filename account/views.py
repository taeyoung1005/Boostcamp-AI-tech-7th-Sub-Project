from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required


def login(request):
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
    if request.method == "POST":
        print(request.POST)
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # 유효한 경우 사용자 저장
            messages.success(request, "Account created successfully. Please log in.")
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

    # 로그아웃 처리
    auth_logout(request)

    return redirect("main:index")
