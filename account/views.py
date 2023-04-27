from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import SignUpSerializer

# Create your views here.


@api_view(["POST"])
def signup(request):
    data = request.data
    serializer = SignUpSerializer(data=data)

    if serializer.is_valid():
        if not User.objects.filter(username=data["email"]).exists():
            user = User.objects.create_user(
                username=data["email"],
                email=data["email"],
                password=make_password(data["password"]),
                first_name=data["first_name"],
                last_name=data["last_name"],
            )
            serializer = SignUpSerializer(user, many=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {"error": "User already exists"}, status=status.HTTP_400_BAD_REQUEST
            )
    else:
        return Response(serializer.errors)
