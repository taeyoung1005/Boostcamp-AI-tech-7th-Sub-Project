from django.contrib import admin
from .models import Notification, Visitor


class NotificationAdmin(admin.ModelAdmin):
    # Admin 리스트 페이지에서 표시할 필드
    list_display = ("user", "title", "message", "created_at", "is_read")

    # 검색 가능한 필드
    search_fields = ("title", "message", "user__username")

    # 필터를 추가할 필드
    list_filter = ("is_read", "created_at")

    # 기본 정렬 설정 (생성 날짜 기준 내림차순)
    ordering = ("-created_at",)


class VisitorAdmin(admin.ModelAdmin):
    # Admin 리스트 페이지에서 표시할 필드
    list_display = ("ip_address", "visit_date")

    # 필터를 추가할 필드
    list_filter = ("visit_date",)

    # 기본 정렬 설정 (방문 날짜 기준 내림차순)
    ordering = ("-visit_date",)


# 커스텀 관리자 클래스 등록
admin.site.register(Notification, NotificationAdmin)
admin.site.register(Visitor, VisitorAdmin)
