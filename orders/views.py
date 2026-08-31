from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from products.models import Product
from .models import Order, OrderItem
from .serializers import CreateOrderSerializer, OrderSerializer
from .utils import generate_upi_qr_png, notify_admin_new_order


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_order_view(request):
    serializer = CreateOrderSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data

    products = {p.id: p for p in Product.objects.filter(id__in=[i["product_id"] for i in data["items"]])}
    total = sum(products[i["product_id"]].price * i["quantity"] for i in data["items"])

    order = Order.objects.create(
        user=request.user,
        full_name=data["full_name"],
        phone=data["phone"],
        address_line=data["address_line"],
        city=data["city"],
        state=data["state"],
        pincode=data["pincode"],
        total_amount=total,
        upi_ref_note=f"ORDER",
    )
    order.upi_ref_note = f"SK-ORDER-{order.id}"
    order.save(update_fields=["upi_ref_note"])

    for i in data["items"]:
        product = products[i["product_id"]]
        OrderItem.objects.create(
            order=order,
            product=product,
            product_name=product.name,
            price=product.price,
            quantity=i["quantity"],
            custom_name=i.get("custom_name", ""),
            custom_subtitle=i.get("custom_subtitle", ""),
        )

    notify_admin_new_order(order)

    return Response(OrderSerializer(order, context={"request": request}).data, status=status.HTTP_201_CREATED)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_orders_view(request):
    orders = Order.objects.filter(user=request.user)
    return Response(OrderSerializer(orders, many=True, context={"request": request}).data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def order_detail_view(request, pk):
    try:
        order = Order.objects.get(pk=pk, user=request.user)
    except Order.DoesNotExist:
        return Response({"detail": "Not found."}, status=404)
    return Response(OrderSerializer(order, context={"request": request}).data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def mark_paid_view(request, pk):
    """Customer confirms they've completed the UPI payment; optionally attaches a screenshot."""
    try:
        order = Order.objects.get(pk=pk, user=request.user)
    except Order.DoesNotExist:
        return Response({"detail": "Not found."}, status=404)

    if "payment_screenshot" in request.FILES:
        order.payment_screenshot = request.FILES["payment_screenshot"]
    order.payment_status = "awaiting_verification"
    order.save()

    return Response(OrderSerializer(order, context={"request": request}).data)


@api_view(["GET"])
def upi_qr_view(request):
    """Returns a PNG UPI QR code for a given amount + optional order id note."""
    try:
        amount = float(request.GET.get("amount", "0"))
    except ValueError:
        amount = 0
    note = request.GET.get("note", "Shree Krishnaa Order")
    png_bytes = generate_upi_qr_png(amount, note)
    return HttpResponse(png_bytes, content_type="image/png")
