from django.contrib import admin
from django.utils.html import format_html

from .models import Order, OrderItem
from .utils import (
    notify_customer_order_confirmed,
    notify_customer_order_shipped,
    notify_customer_order_delivered,
)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ["product", "product_name", "price", "quantity", "custom_name", "custom_subtitle"]
    can_delete = False


@admin.action(description="✅ Verify payment & confirm selected orders")
def verify_and_confirm(modeladmin, request, queryset):
    count = 0
    for order in queryset:
        order.payment_status = "verified"
        order.order_status = "confirmed"
        order.save()
        notify_customer_order_confirmed(order)
        count += 1
    modeladmin.message_user(request, f"{count} order(s) confirmed and customer notified.")


@admin.action(description="📦 Mark as Shipped (notifies customer)")
def mark_shipped(modeladmin, request, queryset):
    count = 0
    for order in queryset:
        order.order_status = "shipped"
        order.save()
        notify_customer_order_shipped(order)
        count += 1
    modeladmin.message_user(request, f"{count} order(s) marked shipped — customer notified by email + SMS.")


@admin.action(description="🎉 Mark as Delivered (notifies customer)")
def mark_delivered(modeladmin, request, queryset):
    count = 0
    for order in queryset:
        order.order_status = "delivered"
        order.save()
        notify_customer_order_delivered(order)
        count += 1
    modeladmin.message_user(request, f"{count} order(s) marked delivered — customer notified.")


@admin.action(description="❌ Reject payment for selected orders")
def reject_payment(modeladmin, request, queryset):
    queryset.update(payment_status="rejected", order_status="cancelled")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
          "id",
    "full_name",
    "phone",
    "product_preview",
    "engraving_summary",
    "total_amount",
    "payment_status",
    "order_status",
    "screenshot_preview",
    "created_at",
    ]
    list_filter = ["payment_status", "order_status", "created_at"]
    search_fields = ["full_name", "phone", "id"]
    inlines = [OrderItemInline]
    actions = [verify_and_confirm, mark_shipped, mark_delivered, reject_payment]
    readonly_fields = ["created_at", "updated_at", "screenshot_preview"]

    def screenshot_preview(self, obj):
        if obj.payment_screenshot:
            return format_html(
                '<a href="{0}" target="_blank"><img src="{0}" style="height:50px;border-radius:6px;" /></a>',
                obj.payment_screenshot.url,
            )
        return "—"
    screenshot_preview.short_description = "Payment Proof"
    def product_preview(self, obj):
    html = []

    for item in obj.items.select_related("product").all():
        if item.product and item.product.image:
            html.append(
                format_html(
                    '''
                    <div style="
                        display:flex;
                        align-items:center;
                        gap:10px;
                        margin-bottom:8px;
                    ">
                        <img
                            src="{}"
                            style="
                                width:60px;
                                height:60px;
                                object-fit:contain;
                                border-radius:6px;
                                border:1px solid #ddd;
                                background:#fff;
                            "
                        />
                        <span>{}</span>
                    </div>
                    ''',
                    item.product.image.url,
                    item.product_name,
                )
            )
        else:
            html.append(
                format_html(
                    '<div>{}</div>',
                    item.product_name,
                )
            )

    return format_html("".join(str(x) for x in html)) if html else "—"

product_preview.short_description = "Product"

    def engraving_summary(self, obj):
        parts = []
        for item in obj.items.all():
            if item.custom_name:
                label = item.custom_name
                if item.custom_subtitle:
                    label += f" / {item.custom_subtitle}"
                parts.append(f"{label} ({item.product_name}, x{item.quantity})")
        return format_html("{}","<br>".join(parts)) if parts else "—"
    engraving_summary.short_description = "What to Engrave"
