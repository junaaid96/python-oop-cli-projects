from __future__ import annotations

from rest_framework import serializers

from .models import Project, Proposal, Skill


class ProjectSerializer(serializers.ModelSerializer):  # type: ignore[type-arg]
    client = serializers.ReadOnlyField(source="client.username")
    skills = serializers.SlugRelatedField(
        many=True, slug_field="name", queryset=Skill.objects.all(), required=False
    )
    proposal_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Project
        fields = (
            "id", "client", "title", "description", "budget",
            "skills", "status", "proposal_count", "created_at",
        )  # fmt: skip
        read_only_fields = ("status",)

    def validate_title(self, value: str) -> str:
        if len(value.strip()) < 5:
            raise serializers.ValidationError("Title must be at least 5 characters.")
        return value.strip()


class ProposalSerializer(serializers.ModelSerializer):  # type: ignore[type-arg]
    freelancer = serializers.ReadOnlyField(source="freelancer.username")

    class Meta:
        model = Proposal
        fields = ("id", "project", "freelancer", "cover_letter", "bid", "status", "created_at")
        read_only_fields = ("project", "status")
