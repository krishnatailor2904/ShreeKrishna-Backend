from django.conf import settings
from django.db import models

from products.models import Product


class Order(models.Model):
    PAYMENT_STATUS = (
        ("pending", "Pending Payment"),
        ("awaiting_verification", "Awaiting Verification"),
        ("verified", "Payment Verified"),
        ("rejected", "Rejected"),
    )
    ORDER_STATUS = (
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("shipped", "Shipped"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="orders", on_delete=models.CASCADE)

    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=15)
    address_line = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)

    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    payment_status = models.CharField(max_length=25, choices=PAYMENT_STATUS, default="pending")
    order_status = models.CharField(max_length=15, choices=ORDER_STATUS, default="pending")
    payment_screenshot = models.ImageField(upload_to="payment_proofs/", blank=True, null=True)
    upi_ref_note = models.CharField(max_length=100, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order #{self.id} — {self.full_name} — ₹{self.total_amount}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="order_items", on_delete=models.SET_NULL, null=True)
    product_name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    # What the customer wants engraved on this specific nameplate/badge
    custom_name = models.CharField(max_length=100, blank=True, help_text="Name to engrave, e.g. 'H.J. Zala'")
    custom_subtitle = models.CharField(max_length=100, blank=True, help_text="Designation/department, e.g. 'P.S.I'")

    @property
    def subtotal(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.product_name} x{self.quantity}"
