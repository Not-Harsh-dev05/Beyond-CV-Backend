"""Explicitly seed clearly marked synthetic demo users and records."""

from datetime import timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.candidates.models import CandidateProfile, EvidenceLink
from apps.jobs.models import JobRole
from apps.scoring.models import ScoreResult
from apps.ingestion.models import SignalSnapshot


class Command(BaseCommand):
    """Create idempotent demo records; never invoked automatically."""

    help = "Seed clearly synthetic demo users, evidence, scores, and a role."

    def handle(self, *args, **options):
        user_model = get_user_model()
        candidate, _ = user_model.objects.get_or_create(
            email="demo.candidate@example.test",
            defaults={"username": "demo_candidate", "role": user_model.Role.CANDIDATE},
        )
        candidate.set_password("DemoCandidate!234")
        candidate.save()
        CandidateProfile.objects.update_or_create(
            user=candidate,
            defaults={
                "name": "Sample Candidate",
                "college_tier": "TIER_3",
                "region": "Sample Region",
                "consent_given": True,
                "is_sample_data": True,
            },
        )
        evidence, _ = EvidenceLink.objects.get_or_create(
            user=candidate,
            source="github",
            handle="sample-account",
            defaults={"ownership_verified": False},
        )
        SignalSnapshot.objects.get_or_create(
            user=candidate,
            source="github",
            defaults={
                "payload": {
                    "method": "sample",
                    "ownership_verified": False,
                    "normalized": 72,
                    "user": {"public_repos": 2},
                    "repositories": [
                        {
                            "name": "sample-project",
                            "description": "Synthetic demo only",
                            "language": "Python",
                        }
                    ],
                },
                "method": "sample",
                "ttl": timedelta(days=1),
                "evidence_link": evidence,
            },
        )
        ScoreResult.objects.get_or_create(
            user=candidate,
            defaults={
                "competence": 72,
                "baseline": 48,
                "delta": 24,
                "baseline_source": "sample_synthetic",
                "warning": "Synthetic demo data; do not treat as a real candidate assessment.",
                "breakdown": {"github": {"score": 72, "weight": 0.65}},
                "sources_used": ["github"],
                "sources_failed": [],
                "ownership_verified": False,
                "is_sample_data": True,
            },
        )
        recruiter, _ = user_model.objects.get_or_create(
            email="demo.recruiter@example.test",
            defaults={"username": "demo_recruiter", "role": user_model.Role.RECRUITER},
        )
        recruiter.set_password("DemoRecruiter!234")
        recruiter.save()
        JobRole.objects.get_or_create(
            recruiter=recruiter,
            title="Sample Backend Engineer",
            defaults={"required_skills": ["Python", "Django"], "is_sample_data": True},
        )
        self.stdout.write(
            self.style.SUCCESS(
                "Seeded synthetic sample data. Login: demo.candidate@example.test / DemoCandidate!234"
            )
        )
