from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from product.models import Product

from .filters import OrderFilter
from .models import Order, OrderItem
from .serializers import OrderSerializer

# Create your views here.


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def new_order(request):
    user = request.user
    data = request.data

    order_items = data["order_items"]

    if order_items and len(order_items) == 0:
        return Response(
            {"detail": "No Order Items"}, status=status.HTTP_400_BAD_REQUEST
        )

    total_amount = 0
    order_items_list = []
    for item in order_items:
        product = get_object_or_404(Product, id=item["product"])
        total_amount += product.price * item["quantity"]
        order_item = OrderItem(product=product, quantity=item["quantity"])
        order_items_list.append(order_item)

    data["total_amount"] = total_amount

    order = Order.objects.create(
        user=user,
        street=data["street"],
        city=data["city"],
        state=data["state"],
        zip=data["zip"],
        phone=data["phone"],
        country=data["country"],
        total_amount=data["total_amount"],
    )

    for order_item in order_items_list:
        order_item.order = order
        order_item.save()
        order.order_items.add(order_item)

    serializer = OrderSerializer(order, many=False)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_orders(request):
    user = request.user
    filterset = OrderFilter(
        request.GET, queryset=Order.objects.filter(user=user).order_by("-id")
    )
    count = filterset.qs.count()
    res_per_page = 10
    paginator = PageNumberPagination()
    paginator.page_size = res_per_page
    queryset = paginator.paginate_queryset(filterset.qs, request)

    serializer = OrderSerializer(queryset, many=True)
    return Response(
        {
            "count": count,
            "next": paginator.get_next_link(),
            "previous": paginator.get_previous_link(),
            "orders": serializer.data,
        }
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_order_by_id(request, pk):
    user = request.user
    order = get_object_or_404(Order, id=pk)

    if user != order.user or user.is_staff == False:
        return Response(
            {"detail": "Not authorized to view this order"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    serializer = OrderSerializer(order, many=False)
    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsAdminUser])
def process_order(request, pk):
    order = get_object_or_404(Order, id=pk)
    data = request.data
    order.order_status = data["order_status"]
    serializer = OrderSerializer(order, many=False)
    return Response(serializer.data)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated | IsAdminUser])
def delete_order(request, pk):
    user = request.user
    order = get_object_or_404(Order, id=pk)

    if user != order.user or user.is_staff == False:
        return Response(
            {"detail": "Not authorized to delete this order"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    order.delete()
    return Response("Order was deleted", status=status.HTTP_204_NO_CONTENT)
