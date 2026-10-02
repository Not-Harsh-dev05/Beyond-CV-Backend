"""Candidate profile and evidence serializers."""

from rest_framework import serializers
from .models import CandidateProfile, EvidenceLink


class CandidateProfileSerializer(serializers.ModelSerializer):
    """Expose only a candidate's editable self-reported profile."""

    class Meta:
        model = CandidateProfile
        exclude = ("id", "user", "created_at", "updated_at")
        read_only_fields = ("self_reported", "is_sample_data")


class EvidenceLinkSerializer(serializers.ModelSerializer):
    """Create source links; ownership state is server-controlled."""

    class Meta:
        model = EvidenceLink
        fields = (
            "id",
            "source",
            "handle",
            "url",
            "verification_code",
            "ownership_verified",
            "created_at",
        )
        read_only_fields = (
            "id",
            "ownership_verified",
            "verification_code",
            "created_at",
        )

    def get_fields(self):
        fields = super().get_fields()
        if self.instance is not None:
            fields["source"].read_only = True
        return fields

    def validate(self, attrs):
        if attrs.get("source") == EvidenceLink.Source.GITHUB and not attrs.get(
            "handle"
        ):
            raise serializers.ValidationError(
                {"handle": "GitHub evidence requires a public username."}
            )
        if attrs.get("source") == EvidenceLink.Source.CERTIFICATE and not attrs.get(
            "url"
        ):
            raise serializers.ValidationError(
                {"url": "Certificate evidence requires a verification URL."}
            )
        return attrs
