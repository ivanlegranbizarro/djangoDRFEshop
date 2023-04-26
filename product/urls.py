from django.urls import path

from . import views

app_name = "product"

urlpatterns = [
    path("", views.get_products, name="products"),
    path("<int:pk>/", views.get_product, name="product_detail"),
]
