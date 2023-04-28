from django.core.validators import MinLengthValidator
from django.db import models

from account.models import MyUser
from product.models import Product

# Create your models here.


class PaymentStatus(models.TextChoices):
    PENDING = ("Pending",)
    COMPLETED = ("Completed",)
    FAILED = ("Failed",)


class OrderStatus(models.TextChoices):
    SHIPPED = ("Shipped",)
    DELIVERED = ("Delivered",)
    CANCELLED = ("Cancelled",)
    PROCESSING = ("Processing",)


class PaymentMode(models.TextChoices):
    COD = ("COD",)
    CARD = ("Card",)
    UPI = ("UPI",)
    NETBANKING = ("Netbanking",)


class Order(models.Model):
    street = models.CharField(max_length=255, validators=[MinLengthValidator(3)])
    city = models.CharField(max_length=255, validators=[MinLengthValidator(3)])
    state = models.CharField(max_length=255, validators=[MinLengthValidator(3)])
    zip = models.CharField(max_length=255, validators=[MinLengthValidator(3)])
    phone = models.CharField(max_length=255, validators=[MinLengthValidator(3)])
    country = models.CharField(max_length=255, validators=[MinLengthValidator(3)])

    total_amount = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)

    payment_status = models.CharField(
        max_length=50, choices=PaymentStatus.choices, default=PaymentStatus.PENDING
    )
    order_status = models.CharField(
        max_length=50, choices=OrderStatus.choices, default=OrderStatus.PROCESSING
    )
    payment_mode = models.CharField(
        max_length=50, choices=PaymentMode.choices, default=PaymentMode.COD
    )
    user = models.ForeignKey(
        MyUser, on_delete=models.SET_NULL, related_name="orders", null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} - {self.created_at}"


class OrderItem(models.Model):
    quantity = models.IntegerField(default=1)
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, related_name="order_items", null=True
    )
    order = models.ForeignKey(
        Order, on_delete=models.SET_NULL, related_name="order_items", null=True
    )

    def __str__(self):
        return f"{self.product.name} - {self.quantity} - {self.product.price}"
