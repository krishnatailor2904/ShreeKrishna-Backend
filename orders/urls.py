from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.create_order_view),
    path("my/", views.my_orders_view),
    path("<int:pk>/", views.order_detail_view),
    path("<int:pk>/mark-paid/", views.mark_paid_view),
    path("upi-qr/", views.upi_qr_view),
]
