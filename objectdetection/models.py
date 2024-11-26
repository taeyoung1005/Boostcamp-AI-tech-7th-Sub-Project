import io
import uuid
import os
import json

from django.db import models
from django.core.files.base import ContentFile
from PIL import Image

from account.models import User


def inference(image) -> json:
    # 임시로 "eagle"로 반환
    # 이미지 분류 모델을 통해 예측 수행
    prediction = {""}
    return json.dumps(prediction)


def objectdetection_image_path(instance, filename):
    # 고유한 파일 이름 생성 (UUID 사용)
    ext = filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join("objectdetection_images", unique_filename)


# Create your models here.
class ObjectDetectionImage(models.Model):
    """
    Object Detection 이미지 모델
    """

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="objectdetection_images"
    )
    objectdetection_image = models.ImageField(
        upload_to=objectdetection_image_path, blank=False, null=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    prediction = models.JSONField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # 이미지가 있는 경우에만 변환
        if self.objectdetection_image:
            img = Image.open(self.objectdetection_image)
            self.prediction = inference(img)

            # WebP 형식으로 변환
            img_io = io.BytesIO()
            img.save(img_io, format="WEBP")

            # 파일을 Django 파일 객체로 설정하여 다시 objectdetection_image에 저장
            webp_image = ContentFile(
                img_io.getvalue(),
                name=f"{self.objectdetection_image.name.split('.')[0]}.webp",
            )
            self.objectdetection_image = webp_image

        super().save(*args, **kwargs)
