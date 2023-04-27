from rest_framework import serializers

from .models import MyUser, Product, Review


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
        extra_kwargs = {"user": {"read_only": True}, "ratings": {"read_only": True}}


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username", read_only=True)
    product = serializers.CharField(source="product.name", read_only=True)

    class Meta:
        model = Review
        fields = "__all__"
