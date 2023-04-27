from django.urls import path

from . import views

app_name = "product"

urlpatterns = [
    path("", views.get_products, name="products"),
    path("detail/<int:pk>", views.get_product, name="product_detail"),
    path("new/", views.new_product, name="new_product"),
    path("update/<int:pk>", views.update_product, name="update_product"),
    path("delete/<int:pk>", views.delete_product, name="delete_product"),
]
