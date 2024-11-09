from django.shortcuts import render, redirect

# Create your views here.


def index(request):
    if request.user.is_authenticated:
        return render(
            request,
            "main/index.html",
            {
                "username": request.user.username,
                "profile_image": request.user.profile_image,
            },
        )
    else:
        return render(request, "main/index.html")
