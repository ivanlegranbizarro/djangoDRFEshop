from rest_framework import serializers
from django.contrib.auth.models import User


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["password", "email", "first_name", "last_name"]

        extra_kwargs = {
            "password": {"write_only": True, "min_length": 6},
            "email": {"required": True},
            "first_name": {"required": True},
            "last_name": {"required": True},
        }


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]
