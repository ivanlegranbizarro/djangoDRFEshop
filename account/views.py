from rest_framework import generics
from rest_framework.permissions import AllowAny

from .models import MyUser
from .serializers import SignUpSerializer


class SignUpView(generics.CreateAPIView):
    queryset = MyUser.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = [AllowAny]
