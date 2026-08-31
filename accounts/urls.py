from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register_view),
    path("login/", views.login_view),
    path("profile/", views.profile_view),
    path("otp/request/", views.request_otp_view),
    path("otp/verify-reset/", views.verify_otp_reset_view),
    path("change-password/", views.change_password_view),
]
