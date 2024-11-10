from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Count

from .models import Notification, Visitor


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def track_visitor(request):
    ip_address = get_client_ip(request)
    today = timezone.now().date()

    # 오늘 방문자 중 동일한 IP가 있는지 확인
    if not Visitor.objects.filter(ip_address=ip_address, visit_date=today).exists():
        # 방문 기록이 없다면 새로운 방문자로 기록
        Visitor.objects.create(ip_address=ip_address, visit_date=today)


def all_visitors():
    all_visitors_count = Visitor.objects.all().count()
    return all_visitors_count


def index(request):
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

    return render(
        request,
        "main/index.html",
        {
            "visitor_counts": visitor_counts,
            "visitor_dates": visitor_dates,
            "all_visitors_count": all_visitors_count,
        },
    )


@login_required(login_url="/account/login/")
def mark_as_read(request, notification_id):
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
    if request.user.is_authenticated:
        Notification.objects.filter(user=request.user, is_read=False).update(
            is_read=True
        )
        return JsonResponse({"success": True})
    return JsonResponse({"success": False}, status=403)


@login_required(login_url="/account/login/")
def get_all_notifications(request):
    notifications = Notification.objects.filter(user=request.user).order_by(
        "-created_at"
    )
    return render(
        request,
        "main/notifications.html",
        {"notifications": notifications},
    )
