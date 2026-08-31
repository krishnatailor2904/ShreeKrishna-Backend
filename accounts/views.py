from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import OTP, User
from .serializers import (
    RegisterSerializer, LoginSerializer, UserSerializer,
    RequestOTPSerializer, VerifyOTPResetSerializer, ChangePasswordSerializer,
)
from .utils import send_otp_email


def tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {"access": str(refresh.access_token), "refresh": str(refresh)}


@api_view(["POST"])
@permission_classes([AllowAny])
def register_view(request):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    return Response({
        "user": UserSerializer(user).data,
        "tokens": tokens_for_user(user),
    }, status=status.HTTP_201_CREATED)


@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data["user"]
    return Response({
        "user": UserSerializer(user).data,
        "tokens": tokens_for_user(user),
    })


@api_view(["GET", "PATCH"])
@permission_classes([IsAuthenticated])
def profile_view(request):
    if request.method == "GET":
        return Response(UserSerializer(request.user).data)
    serializer = UserSerializer(request.user, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([AllowAny])
def request_otp_view(request):
    """Send a password-reset OTP to the given email, if an account exists."""
    serializer = RequestOTPSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data["email"]

    if User.objects.filter(email__iexact=email).exists():
        code = OTP.generate_code()
        OTP.objects.create(email=email.lower(), code=code, purpose="password_reset")
        send_otp_email(email, code, "password_reset")

    # Always return success (don't leak whether the email exists)
    return Response({"detail": "If that email exists, an OTP has been sent."})


@api_view(["POST"])
@permission_classes([AllowAny])
def verify_otp_reset_view(request):
    serializer = VerifyOTPResetSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data

    otp = (
        OTP.objects.filter(email__iexact=data["email"], code=data["code"], purpose="password_reset")
        .order_by("-created_at")
        .first()
    )
    if not otp or not otp.is_valid():
        return Response({"detail": "Invalid or expired OTP."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email__iexact=data["email"])
    except User.DoesNotExist:
        return Response({"detail": "No account with that email."}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(data["new_password"])
    user.save()
    otp.is_used = True
    otp.save()

    return Response({"detail": "Password reset successful. You can now log in."})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def change_password_view(request):
    serializer = ChangePasswordSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = request.user
    if not user.check_password(serializer.validated_data["old_password"]):
        return Response({"detail": "Old password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)
    user.set_password(serializer.validated_data["new_password"])
    user.save()
    return Response({"detail": "Password changed successfully."})
