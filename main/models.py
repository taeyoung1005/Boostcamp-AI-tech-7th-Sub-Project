from django.db import models
from django.utils import timezone

from account.models import User


class Notification(models.Model):
    ICON_CHOICES = [
        ("info", "Info"),
        ("alert", "Alert"),
        ("deposit", "Deposit"),
        ("warning", "Warning"),
        ("success", "Success"),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notifications"
    )
    title = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    icon = models.CharField(
        max_length=50, choices=ICON_CHOICES, default="info"
    )  # 아이콘 종류: 예를 들면 "info", "alert", "deposit"

    def __str__(self):
        return f"{self.title} - {self.user.username}"


class Visitor(models.Model):
    ip_address = models.GenericIPAddressField()
    visit_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"Visitor {self.ip_address} on {self.visit_date}"
