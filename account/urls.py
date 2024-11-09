from django.urls import path

from . import views

app_name = "account"

urlpatterns = [
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout, name="logout"),
    path("profile/update/", views.update_profile, name="update_profile"),
]
