from django.urls import path

from . import views

app_name = "order"

urlpatterns = [
    path("new/", views.new_order, name="new_order"),
    path("get/", views.get_orders, name="get_orders"),
    path("get/<int:pk>/", views.get_order_by_id, name="get_order_by_id"),
    path("delete/<int:pk>/", views.delete_order, name="delete_order"),
    path("process/<int:pk>/", views.process_order, name="process_order"),
]
