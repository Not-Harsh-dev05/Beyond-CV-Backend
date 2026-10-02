"""Candidate self-service and consent-filtered recruiter score access."""

import secrets
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from apps.accounts.permissions import IsCandidateOwner
from apps.core.responses import failure, success
from apps.scoring.models import ScoreResult
from .models import CandidateProfile, EvidenceLink
from .serializers import CandidateProfileSerializer, EvidenceLinkSerializer

User = get_user_model()


class CandidateMeView(APIView):
    """Read, update, or erase the authenticated candidate and owned data."""

    permission_classes = [IsAuthenticated, IsCandidateOwner]

    def get_profile(self, request):
        profile, _ = CandidateProfile.objects.get_or_create(user=request.user)
        self.check_object_permissions(request, profile)
        return profile

    def get(self, request):
        profile = self.get_profile(request)
        data = CandidateProfileSerializer(profile).data
        data["evidence"] = EvidenceLinkSerializer(
            request.user.evidence_links.all(), many=True
        ).data
        return success(data, request=request, is_sample_data=profile.is_sample_data)

    def put(self, request):
        profile = self.get_profile(request)
        if profile.is_sample_data:
            return failure(
                "sample_data_read_only",
                "Synthetic demo profiles cannot be edited.",
                status=403,
                request=request,
            )
        serializer = CandidateProfileSerializer(
            profile, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return success(serializer.data, request=request)

    def delete(self, request):
        profile = self.get_profile(request)
        is_sample_data = profile.is_sample_data
        request.user.delete()
        return success(
            {"deleted": True}, request=request, is_sample_data=is_sample_data
        )


class EvidenceCreateView(APIView):
    """Add an evidence locator to the signed-in candidate."""

    permission_classes = [IsAuthenticated, IsCandidateOwner]

    def post(self, request):
        if request.user.role != "CANDIDATE":
            return failure(
                "forbidden",
                "Only candidates can submit evidence.",
                status=403,
                request=request,
            )
        profile = CandidateProfile.objects.filter(user=request.user).first()
        if profile and profile.is_sample_data:
            return failure(
                "sample_data_read_only",
                "Synthetic demo profiles cannot be edited.",
                status=403,
                request=request,
            )
        serializer = EvidenceLinkSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        challenge = (
            secrets.token_urlsafe(9)[:12]
            if serializer.validated_data["source"] == "github"
            else ""
        )
        evidence = serializer.save(user=request.user, verification_code=challenge)
        self.check_object_permissions(request, evidence)
        return success(
            EvidenceLinkSerializer(evidence).data, status=201, request=request
        )


class EvidenceDetailView(APIView):
    """Edit or remove only evidence owned by the authenticated candidate."""

    permission_classes = [IsAuthenticated, IsCandidateOwner]

    def patch(self, request, evidence_id):
        evidence = get_object_or_404(EvidenceLink, pk=evidence_id)
        self.check_object_permissions(request, evidence)
        if request.user.role != "CANDIDATE":
            return failure(
                "forbidden",
                "Only candidates can edit evidence.",
                status=403,
                request=request,
            )
        if CandidateProfile.objects.filter(
            user=request.user, is_sample_data=True
        ).exists():
            return failure(
                "sample_data_read_only",
                "Synthetic demo profiles cannot be edited.",
                status=403,
                request=request,
            )
        serializer = EvidenceLinkSerializer(evidence, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        changed_locator = any(
            field in serializer.validated_data for field in ("handle", "url")
        )
        evidence = serializer.save()
        if changed_locator:
            evidence.ownership_verified = False
            evidence.verification_code = (
                secrets.token_urlsafe(9)[:12] if evidence.source == "github" else ""
            )
            evidence.snapshots.all().delete()
            evidence.save(update_fields=("ownership_verified", "verification_code"))
        return success(EvidenceLinkSerializer(evidence).data, request=request)

    def delete(self, request, evidence_id):
        evidence = get_object_or_404(EvidenceLink, pk=evidence_id)
        self.check_object_permissions(request, evidence)
        if request.user.role != "CANDIDATE":
            return failure(
                "forbidden",
                "Only candidates can delete evidence.",
                status=403,
                request=request,
            )
        if CandidateProfile.objects.filter(
            user=request.user, is_sample_data=True
        ).exists():
            return failure(
                "sample_data_read_only",
                "Synthetic demo profiles cannot be edited.",
                status=403,
                request=request,
            )
        evidence.delete()
        return success({"deleted": True}, request=request)


class CandidateScoreView(APIView):
    """Return the latest score only to the candidate or a consenting recruiter."""

    permission_classes = [IsAuthenticated]

    def get(self, request, candidate_id):
        user = get_object_or_404(
            User.objects.select_related("candidate_profile"), pk=candidate_id
        )
        if request.user.role == "CANDIDATE" and user.pk != request.user.pk:
            return failure(
                "not_found", "Candidate was not found.", status=404, request=request
            )
        if request.user.role == "RECRUITER":
            self.check_permissions(request)
            if (
                not hasattr(user, "candidate_profile")
                or not user.candidate_profile.consent_given
            ):
                return failure(
                    "not_found", "Candidate was not found.", status=404, request=request
                )
        elif request.user.role not in ("CANDIDATE", "ADMIN"):
            return failure(
                "forbidden",
                "You cannot view candidate scores.",
                status=403,
                request=request,
            )
        result = ScoreResult.objects.filter(user=user).order_by("-computed_at").first()
        if not result:
            return failure(
                "score_unavailable",
                "No score has been computed yet.",
                status=404,
                request=request,
            )
        return success(
            {
                "competence": result.competence,
                "baseline": result.baseline,
                "delta": result.delta,
                "baseline_source": result.baseline_source,
                "warning": result.warning,
                "breakdown": result.breakdown,
                "sources_used": result.sources_used,
                "sources_failed": result.sources_failed,
                "ownership_verified": result.ownership_verified,
                "is_sample_data": result.is_sample_data,
                "computed_at": result.computed_at,
            },
            request=request,
            sources_used=result.sources_used,
            sources_failed=result.sources_failed,
            is_sample_data=result.is_sample_data,
        )
