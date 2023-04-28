from django_filters import rest_framework as filters

from .models import Order


class OrderFilter(filters.FilterSet):
    class Meta:
        model = Order
        fields = ("order_status", "payment_mode", "payment_status")
