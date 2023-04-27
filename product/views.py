from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .filters import ProductsFilter
from .models import Product
from .serializers import ProductSerializer

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
def new_product(request):
    data = request.data

    serializer = ProductSerializer(data=data)

    if serializer.is_valid():
        product = Product.objects.create(**data)
        serializer = ProductSerializer(product, many=False)
        return Response(serializer.data)

    else:
        return Response(serializer.errors)


@api_view(["PUT"])
def update_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    data = request.data

    serializer = ProductSerializer(instance=product, data=data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    else:
        return Response(serializer.errors)
