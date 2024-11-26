from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import ClassificationImage


@login_required(login_url="account:login")
def introduction(request):
    return render(request, "classification/introduction.html")


@login_required(login_url="account:login")
def spaces(request):
    if request.method == "POST":
        if request.FILES.get("image"):
            image = request.FILES.get("image")
            user = request.user

            # Image 모델을 통해 이미지 저장
            image_instance = ClassificationImage(user=user, classification_image=image)
            image_instance.save()

            return render(
                request,
                "classification/spaces.html",
                {
                    "image_url": image_instance.classification_image.url,
                    "prediction": image_instance.prediction,
                    "previous_images": ClassificationImage.objects.all().order_by(
                        "-created_at"
                    )[:30],
                },
            )

    return render(
        request,
        "classification/spaces.html",
        {
            "previous_images": ClassificationImage.objects.all().order_by(
                "-created_at"
            )[:30]
        },
    )
