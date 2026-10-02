"""JWT registration, login, refresh, and logout endpoints."""

from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from apps.core.responses import success
from .serializers import RegisterSerializer, EmailTokenSerializer
from django.contrib.auth import get_user_model


def _is_sample_user(user):
    """Return whether an account's candidate profile is seeded demo data."""
    profile = getattr(user, "candidate_profile", None)
    return bool(profile and profile.is_sample_data)


class RegisterView(generics.CreateAPIView):
    """Register a candidate account and return a response envelope."""

    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "auth"

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return success(
            {"id": user.pk, "email": user.email, "role": user.role},
            status=status.HTTP_201_CREATED,
            request=request,
        )


class LoginView(TokenObtainPairView):
    """Authenticate by email and password."""

    serializer_class = EmailTokenSerializer
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "auth"

    def post(self, request, *args, **kwargs):
        result = super().post(request, *args, **kwargs)
        email = str(request.data.get("email", "")).strip().lower()
        user = get_user_model().objects.filter(email=email).first()
        return success(
            result.data,
            status=result.status_code,
            request=request,
            is_sample_data=bool(user and _is_sample_user(user)),
        )


class RefreshView(TokenRefreshView):
    """Rotate and refresh a JWT."""

    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "auth"

    def post(self, request, *args, **kwargs):
        result = super().post(request, *args, **kwargs)
        token_user = (
            get_user_model()
            .objects.filter(pk=AccessToken(result.data["access"]).get("user_id"))
            .first()
        )
        return success(
            result.data,
            status=result.status_code,
            request=request,
            is_sample_data=bool(token_user and _is_sample_user(token_user)),
        )


class LogoutView(APIView):
    """Blacklist a supplied refresh token."""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        token = request.data.get("refresh")
        if not token:
            from apps.core.responses import failure

            return failure(
                "missing_token",
                "A refresh token is required.",
                status=400,
                request=request,
            )
        try:
            RefreshToken(token).blacklist()
        except TokenError:
            from apps.core.responses import failure

            return failure(
                "invalid_token",
                "Refresh token is invalid or already revoked.",
                status=400,
                request=request,
            )
        return success(
            {"logged_out": True},
            request=request,
            is_sample_data=_is_sample_user(request.user),
        )
