from django.core.validators import (
    MaxValueValidator,
    MinLengthValidator,
    MinValueValidator,
)
from django.db import models
from django.utils.text import slugify

from account.models import MyUser

# Create your models here.


class Category(models.TextChoices):
    ELECTRONICS = ("Electronics",)
    LAPTOPS = ("Laptops",)
    ARTS = ("Arts",)
    FOOD = ("Food",)
    CLOTHING = ("Clothing",)
    HOME = ("Home",)
    KITCHEN = ("Kitchen",)


class Product(models.Model):
    name = models.CharField(
        max_length=100, validators=[MinLengthValidator(3)], unique=True
    )
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)
    description = models.TextField(max_length=500, validators=[MinLengthValidator(10)])
    price = models.DecimalField(max_digits=6, decimal_places=2)
    brand = models.CharField(max_length=50, validators=[MinLengthValidator(3)])
    category = models.CharField(max_length=50, choices=Category.choices)
    ratings = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)
    image1 = models.ImageField(upload_to="products", null=True, blank=True)
    image2 = models.ImageField(upload_to="products", null=True, blank=True)
    image3 = models.ImageField(upload_to="products", null=True, blank=True)
    stock = models.IntegerField(default=0)
    user = models.ForeignKey(
        MyUser, on_delete=models.SET_NULL, related_name="products", null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    constraints = [
        models.CheckConstraint(
            check=models.Q(name__isnull=False) & models.Q(name__exact=""),
            name="name_not_empty",
        ),
        models.CheckConstraint(
            check=models.Q(description__isnull=False) & models.Q(description__exact=""),
            name="description_not_empty",
        ),
    ]

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class Review(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews"
    )
    user = models.ForeignKey(
        MyUser, on_delete=models.CASCADE, related_name="reviews", null=True
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(
        max_length=500, validators=[MinLengthValidator(10)], null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        unique_together = ["product", "user"]

    def __str__(self) -> str:
        return self.comment
