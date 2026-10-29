"""Domain models: clients post Projects, freelancers send Proposals.

Rebuilt from the earlier FreelanceHub interview-prep project, trimmed to the
parts that teach the most: a custom user, choices, FK/M2M relations,
indexes, a constraint, and a custom QuerySet.
"""

from __future__ import annotations

from decimal import Decimal

from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models


class User(AbstractUser):
    """Custom user. Extend AbstractUser (keeps admin, groups, permissions)."""

    class Role(models.TextChoices):
        CLIENT = "CLIENT", "Client"
        FREELANCER = "FREELANCER", "Freelancer"

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.FREELANCER)

    @property
    def is_client(self) -> bool:
        return self.role == self.Role.CLIENT


class Skill(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class ProjectQuerySet(models.QuerySet["Project"]):
    """Reusable, chainable query building blocks (fat models, thin views)."""

    def open(self) -> ProjectQuerySet:
        return self.filter(status=Project.Status.OPEN)

    def with_related(self) -> ProjectQuerySet:
        # select_related -> SQL JOIN for FK; prefetch_related -> 2nd query for M2M.
        return self.select_related("client").prefetch_related("skills")

    def with_proposal_count(self) -> ProjectQuerySet:
        # GROUP BY queries drop Meta.ordering, so order explicitly for stable pages.
        return self.annotate(proposal_count=models.Count("proposals")).order_by("-created_at")


class Project(models.Model):
    class Status(models.TextChoices):
        OPEN = "OPEN", "Open"
        IN_PROGRESS = "IN_PROGRESS", "In progress"
        COMPLETED = "COMPLETED", "Completed"
        CANCELLED = "CANCELLED", "Cancelled"

    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name="projects")
    title = models.CharField(max_length=200)
    description = models.TextField()
    budget = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("1"))]
    )
    skills = models.ManyToManyField(Skill, blank=True, related_name="projects")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = ProjectQuerySet.as_manager()

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["status", "-created_at"])]

    def __str__(self) -> str:
        return self.title


class Proposal(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        ACCEPTED = "ACCEPTED", "Accepted"
        REJECTED = "REJECTED", "Rejected"

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="proposals")
    freelancer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="proposals")
    cover_letter = models.TextField()
    bid = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("1"))]
    )
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            # One proposal per freelancer per project, enforced by the database.
            models.UniqueConstraint(fields=["project", "freelancer"], name="one_proposal_each")
        ]

    def __str__(self) -> str:
        return f"{self.freelancer} -> {self.project}"
