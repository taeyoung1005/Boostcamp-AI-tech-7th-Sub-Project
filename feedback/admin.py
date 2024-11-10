from django.contrib import admin
from .models import Feedback


class FeedbackAdmin(admin.ModelAdmin):
    # Admin 페이지에서 표시할 필드
    list_display = ("title", "author", "created_at", "is_deleted")

    # 필터를 추가할 필드
    list_filter = ("is_deleted", "created_at", "author")

    # 검색할 수 있는 필드 (검색 창에 입력하여 찾기)
    search_fields = ("title", "author__username", "content")


# 커스텀 관리자 클래스 등록
admin.site.register(Feedback, FeedbackAdmin)
