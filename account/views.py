from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import MyUser
from .serializers import SignUpSerializer


class SignUpView(generics.CreateAPIView):
    queryset = MyUser.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = [AllowAny]


class CurrentUserView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MyUser.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
