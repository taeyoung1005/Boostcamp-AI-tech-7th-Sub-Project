# urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import CustomPasswordResetForm, CustomSetPasswordForm


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("main.urls")),
    path("account/", include("account.urls")),
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(form_class=CustomPasswordResetForm),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(form_class=CustomSetPasswordForm),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
