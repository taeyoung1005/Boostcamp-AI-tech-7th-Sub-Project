from django.urls import path

from . import views

app_name = "main"

urlpatterns = [
    path("", views.index, name="index"),
    path(
        "notifications/read/<int:notification_id>/",
        views.mark_as_read,
        name="mark_as_read",
    ),
    path(
        "notifications/unread/",
        views.get_unread_notifications,
        name="get_unread_notifications",
    ),
    path("notifications/read_all/", views.mark_all_as_read, name="mark_all_as_read"),
    path(
        "notifications/all/", views.get_all_notifications, name="get_all_notifications"
    ),
]
