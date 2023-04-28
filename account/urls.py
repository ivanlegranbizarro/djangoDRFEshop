from django.urls import path

from . import views

app_name = "account"

urlpatterns = [
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("me/", views.CurrentUserView.as_view(), name="user"),
    path("forgot-password", views.forgot_password, name="forgot_password"),
    path("reset-password", views.reset_password, name="reset_password"),
]
