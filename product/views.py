from django.db import IntegrityError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .filters import ProductsFilter
from .models import Product, Review
from .serializers import ProductSerializer, ReviewSerializer

# Create your views here.


@api_view(["GET"])
def get_products(request):
    filterset = ProductsFilter(
        request.GET, queryset=Product.objects.all().order_by("-id")
    )
    count = filterset.qs.count()
    res_per_page = 10
    paginator = PageNumberPagination()
    paginator.page_size = res_per_page

    result_page = paginator.paginate_queryset(filterset.qs, request)
    serializer = ProductSerializer(result_page, many=True)

    return Response(
        {
            "count": count,
            "next": paginator.get_next_link(),
            "previous": paginator.get_previous_link(),
            "products": serializer.data,
        }
    )


@api_view(["GET"])
def get_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def new_product(request):
    data = request.data

    serializer = ProductSerializer(data=data)

    if serializer.is_valid():
        product = Product.objects.create(**data, user=request.user)
        serializer = ProductSerializer(product, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    else:
        return Response(serializer.errors)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.user != product.user:
        return Response(
            {"error": "You do not have permission to perform this action."},
            status=status.HTTP_403_FORBIDDEN,
        )

    data = request.data

    serializer = ProductSerializer(instance=product, data=data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    else:
        return Response(serializer.errors)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.user != product.user:
        return Response(
            {"error": "You do not have permission to perform this action."},
            status=status.HTTP_403_FORBIDDEN,
        )
    product.delete()
    return Response("Product deleted successfully", status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_review(request, pk):
    user = request.user
    product = get_object_or_404(Product, pk=pk)
    data = request.data
    data["user"] = user.id
    data["product"] = product.id

    serializer = ReviewSerializer(data=data)

    if serializer.is_valid():
        try:
            review = serializer.save(user=user, product=product)
            serializer = ReviewSerializer(review, many=False)
            rating = product.reviews.aggregate(Avg("rating"))["rating__avg"]
            product.ratings = rating
            product.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response(
                {"error": "You have already reviewed this product."},
                status=status.HTTP_400_BAD_REQUEST,
            )

    return Response(serializer.errors)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_review(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.user != review.user:
        return Response(
            {"error": "You do not have permission to perform this action."},
            status=status.HTTP_403_FORBIDDEN,
        )
    data = request.data

    serializer = ReviewSerializer(instance=review, data=data, partial=True)

    if serializer.is_valid():
        serializer.save()

        product = review.product
        rating = product.reviews.aggregate(Avg("rating"))["rating__avg"]
        product.ratings = rating
        product.save()

        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    else:
        return Response(serializer.errors)
