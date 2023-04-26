from django.contrib import admin

from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ("slug", "created_at", "updated_at")
    list_display = (
        "id",
        "name",
        "slug",
        "price",
        "brand",
        "category",
        "created_at",
    )
    list_filter = ("category", "brand", "created_at")
