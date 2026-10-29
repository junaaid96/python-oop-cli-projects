"""Service layer: business rules live here, not in views or serializers.

Views (HTML or API) call these functions, so both share one source of truth
and the rules are easy to unit-test.
"""

from __future__ import annotations

from decimal import Decimal

from django.db import transaction

from .models import Project, Proposal, User


class BusinessRuleError(Exception):
    """Raised when an action breaks a domain rule (mapped to HTTP 400)."""


def submit_proposal(
    *, project: Project, freelancer: User, cover_letter: str, bid: Decimal
) -> Proposal:
    if freelancer.is_client:
        raise BusinessRuleError("Only freelancers can submit proposals.")
    if project.status != Project.Status.OPEN:
        raise BusinessRuleError("This project is not accepting proposals.")
    if project.client_id == freelancer.pk:
        raise BusinessRuleError("You cannot bid on your own project.")
    if Proposal.objects.filter(project=project, freelancer=freelancer).exists():
        raise BusinessRuleError("You already sent a proposal for this project.")
    return Proposal.objects.create(
        project=project, freelancer=freelancer, cover_letter=cover_letter, bid=bid
    )


@transaction.atomic
def accept_proposal(*, proposal: Proposal, by: User) -> Proposal:
    """Accept one proposal, reject the rest, start the project. All or nothing."""
    # select_for_update locks the row so two requests cannot both accept.
    project = Project.objects.select_for_update().get(pk=proposal.project_id)
    if project.client_id != by.pk:
        raise BusinessRuleError("Only the project owner can accept proposals.")
    if project.status != Project.Status.OPEN:
        raise BusinessRuleError("This project already has an accepted proposal.")
    project.proposals.exclude(pk=proposal.pk).update(status=Proposal.Status.REJECTED)
    proposal.status = Proposal.Status.ACCEPTED
    proposal.save(update_fields=["status"])
    project.status = Project.Status.IN_PROGRESS
    project.save(update_fields=["status"])
    return proposal
