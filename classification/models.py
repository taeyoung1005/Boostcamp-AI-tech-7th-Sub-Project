import io
import uuid
import os
import json

from django.db import models
from django.core.files.base import ContentFile
from PIL import Image

from account.models import User


def inference(image):
    # 임시로 "eagle"로 반환
    # 이미지 분류 모델을 통해 예측 수행
    prediction = {"eagle": 0.7, "owl": 0.4, "parrot": 0.2, "penguin": 0, "duck": 0.1}
    return json.dumps(prediction)


def classification_image_path(instance, filename):
    # 고유한 파일 이름 생성 (UUID 사용)
    ext = filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join("classification_images", unique_filename)


# Create your models here.
class ClassificationImage(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="classification_images"
    )
    classification_image = models.ImageField(
        upload_to=classification_image_path,
        blank=False,
        null=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    prediction = models.CharField(max_length=100, blank=True)

    def save(self, *args, **kwargs):
        # 이미지가 있는 경우에만 변환
        if self.classification_image:
            img = Image.open(self.classification_image)
            self.prediction = inference(img)

            # WebP 형식으로 변환
            img_io = io.BytesIO()
            img.save(img_io, format="WEBP")

            # 파일을 Django 파일 객체로 설정하여 다시 classification_image에 저장
            webp_image = ContentFile(
                img_io.getvalue(),
                name=f"{self.classification_image.name.split('.')[0]}.webp",
            )
            self.classification_image = webp_image

        super().save(*args, **kwargs)
