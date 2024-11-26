from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Count

from .models import Notification, Visitor
from classification.models import ClassificationImage
from objectdetection.models import ObjectDetectionImage


def get_client_ip(request):
    """
    클라이언트의 IP 주소를 반환합니다.
    """
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def track_visitor(request):
    """
    방문자를 추적하고, 오늘 방문한 방문자를 기록합니다.
    """
    ip_address = get_client_ip(request)
    today = timezone.now().date()

    # 오늘 방문자 중 동일한 IP가 있는지 확인
    if not Visitor.objects.filter(ip_address=ip_address, visit_date=today).exists():
        # 방문 기록이 없다면 새로운 방문자로 기록
        Visitor.objects.create(ip_address=ip_address, visit_date=today)


def all_visitors():
    """
    전체 방문자 수를 반환합니다.
    """

    all_visitors_count = Visitor.objects.all().count()
    return all_visitors_count


def all_images():
    """
    전체 이미지 수를 반환합니다.
    """
    cls_images_count = ClassificationImage.objects.all().count()
    obj_images_count = ObjectDetectionImage.objects.all().count()
    ocr_images_count = 0
    seg_images_count = 0

    task_images_count = [
        cls_images_count,
        obj_images_count,
        ocr_images_count,
        seg_images_count,
    ]
    return task_images_count


def index(request):
    """
    메인 Dashboard 페이지를 보여주는 뷰입니다.
    """
    track_visitor(request)

    # 방문자 수 데이터 생성 (최근 7일 기준)
    last_week = timezone.now().date() - timezone.timedelta(days=7)
    visitor_data = (
        Visitor.objects.filter(visit_date__gte=last_week)
        .values("visit_date")
        .annotate(count=Count("id"))
        .order_by("visit_date")
    )
    visitor_counts = [entry["count"] for entry in visitor_data]
    visitor_dates = [entry["visit_date"].strftime("%Y-%m-%d") for entry in visitor_data]
    all_visitors_count = all_visitors()
    all_images_count = all_images()

    return render(
        request,
        "main/index.html",
        {
            "visitor_counts": visitor_counts,
            "visitor_dates": visitor_dates,
            "all_visitors_count": all_visitors_count,
            "all_images_count": sum(all_images_count),
            "task_images_count": all_images_count,
        },
    )


@login_required(login_url="/account/login/")
def mark_as_read(request, notification_id):
    """
    특정 알림을 읽은 상태로 표시합니다. 로그인한 사용자만 접근할 수 있습니다.
    """
    if request.user.is_authenticated:
        notification = get_object_or_404(
            Notification, id=notification_id, user=request.user
        )
        notification.is_read = True
        notification.save()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False}, status=403)


@login_required(login_url="/account/login/")
def get_unread_notifications(request):
    """
    읽지 않은 알림 목록을 반환합니다. 로그인한 사용자만 접근할 수 있습니다.
    """
    if request.user.is_authenticated:
        unread_notifications = Notification.objects.filter(
            user=request.user, is_read=False
        ).order_by("-created_at")
        notifications_data = [
            {
                "id": notification.id,
                "title": notification.title,
                "created_at": notification.created_at.strftime("%Y %B %d %H:%M:%S"),
                "is_read": notification.is_read,
                "icon": notification.icon,
            }
            for notification in unread_notifications
        ]
        return JsonResponse(
            {"notifications": notifications_data, "count": len(notifications_data)}
        )
    return JsonResponse({"error": "Unauthorized"}, status=401)


@login_required(login_url="/account/login/")
def mark_all_as_read(request):
    """
    모든 알림을 읽은 상태로 표시합니다. 로그인한 사용자만 접근할 수 있습니다.
    """
    if request.user.is_authenticated:
        Notification.objects.filter(user=request.user, is_read=False).update(
            is_read=True
        )
        return JsonResponse({"success": True})
    return JsonResponse({"success": False}, status=403)


@login_required(login_url="/account/login/")
def get_all_notifications(request):
    """
    모든 알림 목록을 반환합니다. 로그인한 사용자만 접근할 수 있습니다.
    """
    notifications = Notification.objects.filter(user=request.user).order_by(
        "-created_at"
    )
    return render(
        request,
        "main/notifications.html",
        {"notifications": notifications},
    )
