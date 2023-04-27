from .models import MyUser
from rest_framework import serializers


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ["email", "password", "first_name", "last_name", "username"]

        extra_kwargs = {
            "password": {"write_only": True, "min_length": 6},
            "email": {"required": True},
            "first_name": {"required": True},
            "last_name": {"required": True},
            "username": {"required": True},
        }
