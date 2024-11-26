from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
from .models import ObjectDetectionImage


@login_required(login_url="account:login")
def introduction(request):
    return render(request, "objectdetection/introduction.html")


@login_required(login_url="account:login")
def spaces(request):
    if request.method == "POST":
        if request.FILES.get("image"):
            image = request.FILES.get("image")
            user = request.user

            # Image 모델을 통해 이미지 저장
            image_instance = ObjectDetectionImage(
                user=user, objectdetection_image=image
            )
            image_instance.save()
    return render(request, "objectdetection/spaces.html")
