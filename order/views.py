from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from product.models import Product

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
    orders = Order.objects.filter(user=user)
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_order_by_id(request, pk):
    user = request.user
    order = Order.objects.get(id=pk)
    serializer = OrderSerializer(order, many=False)
    return Response(serializer.data)
