"""Authentication request/response serializers."""

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    """Create candidate-only accounts; role is not client controlled."""

    password = serializers.CharField(write_only=True, min_length=10)

    class Meta:
        model = User
        fields = ("id", "email", "username", "password")

    def validate_email(self, value):
        return value.strip().lower()

    def create(self, validated_data):
        return User.objects.create_user(role=User.Role.CANDIDATE, **validated_data)


class EmailTokenSerializer(TokenObtainPairSerializer):
    """JWT claims include the application role."""

    username_field = User.EMAIL_FIELD

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["role"] = user.role
        profile = getattr(user, "candidate_profile", None)
        token["is_sample_data"] = bool(profile and profile.is_sample_data)
        return token
