import datetime
from datetime import timedelta

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.crypto import get_random_string
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from .models import MyUser
from .serializers import SignUpSerializer


class SignUpView(generics.CreateAPIView):
    queryset = MyUser.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = [AllowAny]


class CurrentUserView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MyUser.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = [IsAuthenticated | IsAdminUser]

    def get_object(self):
        return self.request.user


def get_current_host(request):
    protocol = request.is_secure() and "https" or "http"
    host = request.get_host()
    return f"{protocol}://{host}"


@api_view(["POST"])
def forgot_password(request):
    data = request.data
    user = get_object_or_404(MyUser, email=data["email"])
    token = get_random_string(40)
    user.profile.reset_password_token = token
    user.profile.reset_password_expire = timezone.now() + timedelta(minutes=30)

    user.profile.save()

    host = get_current_host(request)

    link = f"{host}api/account/forgot-password/{token}"

    body = f"Hi {user.first_name},\n\nPlease click on the link below to reset your password:\n\n{link}\n\nThanks,\n\nTeam"

    send_mail(
        "Reset Password from eshopdjango",
        body,
        "noreplay@eshopdjango.com",
        [user.email],
    )

    return Response({"message": "Email sent"}, status=status.HTTP_200_OK)


@api_view(["POST"])
def reset_password(request, token):
    data = request.data
    user = get_object_or_404(MyUser, profile__reset_password_token=token)

    if user.profile.reset_password_expire.replace(tzinfo=None) < datetime.now():
        return Response(
            {"message": "Token expired"}, status=status.HTTP_400_BAD_REQUEST
        )

    if data["password"] != data["confirm_password"]:
        return Response(
            {"message": "Passwords do not match"}, status=status.HTTP_400_BAD_REQUEST
        )

    user.set_password(data["password"])
    user.profile.reset_password_token = ""
    user.profile.reset_password_expire = ""

    user.profile.save()
    user.save()

    return Response({"message": "Password reset successfully"})
