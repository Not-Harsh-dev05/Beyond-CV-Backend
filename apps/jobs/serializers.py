"""Job-role input validation and representation."""

from math import isfinite

from rest_framework import serializers
from .models import JobRole


class JobRoleSerializer(serializers.ModelSerializer):
    """Create jobs with a non-empty skill list."""

    class Meta:
        model = JobRole
        fields = (
            "id",
            "title",
            "description",
            "required_skills",
            "skill_weights",
            "is_sample_data",
            "created_at",
        )
        read_only_fields = ("id", "is_sample_data", "created_at")

    def validate_required_skills(self, value):
        if (
            not isinstance(value, list)
            or not value
            or any(not isinstance(skill, str) or not skill.strip() for skill in value)
        ):
            raise serializers.ValidationError(
                "Provide a non-empty list of skill names."
            )
        return [skill.strip() for skill in value]

    def validate_skill_weights(self, value):
        if not isinstance(value, dict) or any(
            isinstance(weight, bool)
            or not isinstance(weight, (int, float))
            or not isfinite(weight)
            or weight < 0
            for weight in value.values()
        ):
            raise serializers.ValidationError(
                "Skill weights must be a mapping of names to non-negative numbers."
            )
        return value

    def validate(self, attrs):
        skills = [skill.lower() for skill in attrs.get("required_skills", [])]
        weights = {
            key.lower(): weight
            for key, weight in attrs.get("skill_weights", {}).items()
        }
        if skills and all(weights.get(skill, 1) == 0 for skill in skills):
            raise serializers.ValidationError(
                {
                    "skill_weights": "At least one required skill must have positive weight."
                }
            )
        return attrs
