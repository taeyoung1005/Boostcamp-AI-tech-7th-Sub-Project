from django.contrib import admin
from .models import User  # models.py에 정의된 User 모델을 임포트


# 모델 등록
class UserAdmin(admin.ModelAdmin):
    # Admin 리스트 페이지에서 표시할 필드
    list_display = (
        "email",
        "username",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
    )

    # Admin 리스트 페이지에서 검색 가능한 필드
    search_fields = ("email", "username", "first_name", "last_name")

    # Admin 리스트 페이지에서 필터를 추가할 필드
    list_filter = ("is_staff", "is_active", "created_at")

    # 각 필드를 수정할 수 있는 입력란을 필드셋으로 구분
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Personal Info",
            {"fields": ("username", "first_name", "last_name", "bio", "profile_image")},
        ),
        (
            "Permissions",
            {"fields": ("is_staff", "is_active", "is_superuser", "user_permissions")},
        ),
        ("Important dates", {"fields": ("last_login", "created_at", "updated_at")}),
    )

    # 'created_at' 및 'updated_at' 필드만 읽기 전용으로 설정
    readonly_fields = ("created_at", "updated_at", "last_login")


# 커스텀 관리자 클래스 등록
admin.site.register(User, UserAdmin)
