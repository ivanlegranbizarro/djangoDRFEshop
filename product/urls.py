from django.urls import path

from . import views

app_name = "product"

urlpatterns = [
    path("", views.get_products, name="products"),
    path("detail/<int:pk>", views.get_product, name="product_detail"),
    path("new/", views.new_product, name="new_product"),
]
