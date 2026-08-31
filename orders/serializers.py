from rest_framework import serializers
from products.models import Product
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["id", "product", "product_name", "price", "quantity", "custom_name", "custom_subtitle"]


class OrderItemInputSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)
    custom_name = serializers.CharField(max_length=100, required=False, allow_blank=True, default="")
    custom_subtitle = serializers.CharField(max_length=100, required=False, allow_blank=True, default="")


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id", "full_name", "phone", "address_line", "city", "state", "pincode",
            "total_amount", "payment_status", "order_status", "payment_screenshot",
            "upi_ref_note", "created_at", "items",
        ]
        read_only_fields = ["total_amount", "payment_status", "order_status", "created_at"]


class CreateOrderSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=150)
    phone = serializers.CharField(max_length=15)
    address_line = serializers.CharField(max_length=255)
    city = serializers.CharField(max_length=100)
    state = serializers.CharField(max_length=100)
    pincode = serializers.CharField(max_length=10)
    items = OrderItemInputSerializer(many=True)

    def validate_items(self, items):
        if not items:
            raise serializers.ValidationError("Cart is empty.")
        for item in items:
            if not Product.objects.filter(id=item["product_id"], is_active=True).exists():
                raise serializers.ValidationError(f"Product {item['product_id']} not found.")
        return items
