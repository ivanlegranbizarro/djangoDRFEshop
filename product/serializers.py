from rest_framework import serializers

from .models import Product, Review


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username", read_only=True)
    product = serializers.CharField(source="product.name", read_only=True)

    class Meta:
        model = Review
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    user = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Product
        fields = (
            "id",
            "user",
            "name",
            "description",
            "price",
            "category",
            "brand",
            "stock",
            "image1",
            "image2",
            "image3",
            "ratings",
            "reviews",
        )
        extra_kwargs = {"user": {"read_only": True}, "ratings": {"read_only": True}}
