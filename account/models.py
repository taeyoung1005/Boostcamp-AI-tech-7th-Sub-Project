import io
import os
import uuid

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.core.files.base import ContentFile
from PIL import Image


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


def profile_image_path(instance, filename):
    # 고유한 파일 이름 생성 (UUID 사용)
    ext = filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4()}.{ext}"
    # "profile_images/{user_id}/filename.webp" 형식으로 저장
    return os.path.join("profile_images", unique_filename)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(
        upload_to=profile_image_path,
        blank=True,
        null=True,
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        # 프로필 이미지가 있는 경우에만 변환
        if self.profile_image:
            # 이미지를 열고 WebP 형식으로 변환
            img = Image.open(self.profile_image)
            img_io = io.BytesIO()
            img.save(img_io, format="WEBP")

            # 파일을 Django 파일 객체로 설정하여 다시 profile_image에 저장
            webp_image = ContentFile(
                img_io.getvalue(), name=f"{self.profile_image.name.split('.')[0]}.webp"
            )
            self.profile_image = webp_image

        super().save(*args, **kwargs)
