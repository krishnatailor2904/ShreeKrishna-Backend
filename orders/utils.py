import io
import urllib.parse

import qrcode
import requests
from django.conf import settings
from django.core.mail import send_mail


def build_upi_link(amount, note="Shree Krishnaa Order"):
    """Build a standard UPI deep link that any UPI app (GPay/PhonePe/Paytm) can scan & pay."""
    params = {
        "pa": settings.UPI_ID,               # payee address (your UPI ID)
        "pn": settings.UPI_PAYEE_NAME,       # payee name
        "am": f"{amount:.2f}",               # amount
        "cu": "INR",
        "tn": note,                          # transaction note
    }
    return "upi://pay?" + urllib.parse.urlencode(params)


def generate_upi_qr_png(amount, note="Shree Krishnaa Order"):
    """Returns raw PNG bytes of a scannable UPI QR code for the given amount."""
    link = build_upi_link(amount, note)
    img = qrcode.make(link, box_size=10, border=2)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def send_sms(phone, message):
    """Send an SMS via Fast2SMS. No-ops silently if no API key is configured."""
    api_key = settings.FAST2SMS_API_KEY
    if not api_key or not phone:
        return False
    try:
        requests.post(
            "https://www.fast2sms.com/dev/bulkV2",
            headers={"authorization": api_key},
            data={
                "route": "q",
                "message": message,
                "language": "english",
                "flash": 0,
                "numbers": phone,
            },
            timeout=10,
        )
        return True
    except requests.RequestException:
        return False


def notify_admin_new_order(order):
    """Alert the shop owner (email + SMS) as soon as a new order is placed."""
    items_text = "\n".join(
        f"  - {item.product_name} x{item.quantity} = Rs.{item.subtotal}"
        + (f"\n      Engrave: \"{item.custom_name}\"" + (f" / \"{item.custom_subtitle}\"" if item.custom_subtitle else "") if item.custom_name else "")
        for item in order.items.all()
    )
    subject = f"🛍️ New Order #{order.id} — Shree Krishnaa"
    body = (
        f"New order received!\n\n"
        f"Order ID: #{order.id}\n"
        f"Customer: {order.full_name} ({order.phone})\n"
        f"Address: {order.address_line}, {order.city}, {order.state} - {order.pincode}\n\n"
        f"Items:\n{items_text}\n\n"
        f"Total: Rs.{order.total_amount}\n"
        f"Payment status: {order.get_payment_status_display()}\n\n"
        f"Review & approve payment in the admin panel."
    )

    if settings.ADMIN_NOTIFY_EMAIL:
        try:
            send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [settings.ADMIN_NOTIFY_EMAIL], fail_silently=True)
        except Exception:
            pass

    if settings.ADMIN_NOTIFY_PHONE:
        sms_text = (
            f"New order #{order.id} from {order.full_name} ({order.phone}) "
            f"for Rs.{order.total_amount}. Check admin panel - Shree Krishnaa"
        )
        send_sms(settings.ADMIN_NOTIFY_PHONE, sms_text)


def notify_customer_order_confirmed(order):
    subject = f"Your Shree Krishnaa order #{order.id} is confirmed!"
    body = (
        f"Hi {order.full_name},\n\n"
        f"Great news — your payment has been verified and order #{order.id} "
        f"is now confirmed. We'll start preparing your engraving and ship it soon!\n\n"
        f"Total paid: Rs.{order.total_amount}\n\n"
        f"Thank you for shopping with Shree Krishnaa 🙏"
    )
    try:
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [order.user.email], fail_silently=True)
    except Exception:
        pass


def notify_customer_order_shipped(order):
    subject = f"📦 Your Shree Krishnaa order #{order.id} has been shipped!"
    body = (
        f"Hi {order.full_name},\n\n"
        f"Your order #{order.id} has been shipped and is on its way to:\n"
        f"{order.address_line}, {order.city}, {order.state} - {order.pincode}\n\n"
        f"Total: Rs.{order.total_amount}\n\n"
        f"Thank you for shopping with Shree Krishnaa 🙏"
    )
    try:
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [order.user.email], fail_silently=True)
    except Exception:
        pass
    sms_text = f"Shree Krishnaa: Your order #{order.id} has been shipped! Thank you for shopping with us."
    send_sms(order.phone, sms_text)


def notify_customer_order_delivered(order):
    subject = f"Your Shree Krishnaa order #{order.id} has been delivered"
    body = (
        f"Hi {order.full_name},\n\n"
        f"Your order #{order.id} has been marked as delivered. We hope you love it!\n\n"
        f"If anything is wrong with your order, just reply to this email and we'll sort it out.\n\n"
        f"Thank you for shopping with Shree Krishnaa 🙏"
    )
    try:
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [order.user.email], fail_silently=True)
    except Exception:
        pass
