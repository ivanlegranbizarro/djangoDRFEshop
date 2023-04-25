from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.text import slugify

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
    name = models.CharField(max_length=100, validators=[MinLengthValidator(3)])
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)
    description = models.TextField(max_length=500, validators=[MinLengthValidator(10)])
    price = models.DecimalField(max_digits=6, decimal_places=2)
    brand = models.CharField(max_length=50, validators=[MinLengthValidator(3)])
    category = models.CharField(max_length=50, choices=Category.choices)
    ratings = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)
    stock = models.IntegerField(default=0)
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="products", null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name
