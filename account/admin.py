from django.contrib import admin
from .models import User  # models.py에 정의된 User 모델을 임포트

# 모델 등록
admin.site.register(User)
