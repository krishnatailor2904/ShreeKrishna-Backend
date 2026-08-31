from django.conf import settings
from django.core.mail import send_mail


def send_otp_email(email, code, purpose="password_reset"):
    if purpose == "password_reset":
        subject = "Shree Krishnaa — Password Reset OTP"
        message = (
            f"Your OTP to reset your Shree Krishnaa account password is: {code}\n\n"
            f"This code is valid for 10 minutes. If you did not request this, "
            f"please ignore this email."
        )
    else:
        subject = "Shree Krishnaa — Verify your account"
        message = f"Your verification code is: {code}\nValid for 10 minutes."

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL or "no-reply@shreekrishnaa.com",
        [email],
        fail_silently=False,
    )
