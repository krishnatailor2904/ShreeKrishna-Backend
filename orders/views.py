import uuid

from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from products.models import Product
from .models import Order, OrderItem
from .serializers import CreateOrderSerializer, OrderSerializer
from .utils import generate_upi_qr_png, notify_admin_new_order


@api_view(["POST"])
@permission_classes([AllowAny])
def create_order_view(request):
    serializer = CreateOrderSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data

    products = {p.id: p for p in Product.objects.filter(id__in=[i["product_id"] for i in data["items"]])}
    total = sum(products[i["product_id"]].price * i["quantity"] for i in data["items"])

    # Logged-in user ho to uske saath order link hoga, warna guest order ban jaayega.
    is_guest = not request.user.is_authenticated
    order = Order.objects.create(
        user=None if is_guest else request.user,
        guest_token=uuid.uuid4().hex if is_guest else "",
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


def _get_order_for_request(request, pk):
    """Fetch an order the current request is allowed to touch: the owning
    logged-in user, or a guest with the matching guest_token."""
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return None

    if request.user.is_authenticated:
        if order.user_id == request.user.id:
            return order
        return None

    token = request.data.get("guest_token") or request.GET.get("guest_token")
    if order.guest_token and token == order.guest_token:
        return order
    return None


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_orders_view(request):
    orders = Order.objects.filter(user=request.user)
    return Response(OrderSerializer(orders, many=True, context={"request": request}).data)


@api_view(["POST"])
@permission_classes([AllowAny])
def guest_orders_view(request):
    """Guest 'My Orders': browser apne orders ki [{id, token}] list bhejta hai,
    sirf wahi orders wapas aate hain jinka id + token dono match kare."""
    entries = request.data.get("orders") or []
    if not isinstance(entries, list):
        return Response([])

    matched = []
    for entry in entries[:50]:
        if not isinstance(entry, dict):
            continue
        try:
            order = Order.objects.get(pk=int(entry.get("id")))
        except (Order.DoesNotExist, TypeError, ValueError):
            continue
        token = entry.get("token")
        if order.guest_token and token == order.guest_token:
            matched.append(order)

    matched.sort(key=lambda o: o.created_at, reverse=True)
    return Response(OrderSerializer(matched, many=True, context={"request": request}).data)


@api_view(["GET"])
@permission_classes([AllowAny])
def order_detail_view(request, pk):
    order = _get_order_for_request(request, pk)
    if order is None:
        return Response({"detail": "Not found."}, status=404)
    return Response(OrderSerializer(order, context={"request": request}).data)


@api_view(["POST"])
@permission_classes([AllowAny])
def mark_paid_view(request, pk):
    """Customer confirms they've completed the UPI payment; optionally attaches a screenshot."""
    order = _get_order_for_request(request, pk)
    if order is None:
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