"""pytest-django tests: models, services, HTML views and the DRF API."""

from __future__ import annotations

from decimal import Decimal

import pytest
from django.db import IntegrityError, connection
from django.test import Client
from django.test.utils import CaptureQueriesContext
from marketplace import services
from marketplace.models import Project, Proposal, Skill, User
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db


@pytest.fixture
def client_user() -> User:
    return User.objects.create_user("ada", "ada@example.com", "pw-12345!", role=User.Role.CLIENT)


@pytest.fixture
def freelancer() -> User:
    return User.objects.create_user("linus", "linus@example.com", "pw-12345!")


@pytest.fixture
def project(client_user: User) -> Project:
    p = Project.objects.create(
        client=client_user, title="Build a REST API", description="DRF please", budget=500
    )
    p.skills.add(Skill.objects.create(name="django"))
    return p


@pytest.fixture
def api() -> APIClient:
    return APIClient()


# --- models & ORM -----------------------------------------------------------


def test_open_queryset_filters_status(project: Project) -> None:
    Project.objects.create(
        client=project.client, title="Old job here", description="x", budget=10,
        status=Project.Status.COMPLETED,
    )  # fmt: skip
    assert list(Project.objects.open()) == [project]


def test_with_proposal_count_annotates(project: Project, freelancer: User) -> None:
    Proposal.objects.create(project=project, freelancer=freelancer, cover_letter="hi", bid=400)
    assert Project.objects.with_proposal_count().get(pk=project.pk).proposal_count == 1  # type: ignore[attr-defined]


def test_unique_proposal_constraint(project: Project, freelancer: User) -> None:
    Proposal.objects.create(project=project, freelancer=freelancer, cover_letter="a", bid=1)
    with pytest.raises(IntegrityError):
        Proposal.objects.create(project=project, freelancer=freelancer, cover_letter="b", bid=2)


def test_with_related_avoids_n_plus_one(client_user: User) -> None:
    for i in range(5):
        p = Project.objects.create(
            client=client_user, title=f"Project {i}", description="d", budget=10
        )
        p.skills.add(Skill.objects.create(name=f"s{i}"))
    with CaptureQueriesContext(connection) as ctx:
        for p in Project.objects.with_related():
            _ = p.client.username, [s.name for s in p.skills.all()]
    assert len(ctx.captured_queries) == 2  # 1 JOIN query + 1 prefetch query


# --- services -----------------------------------------------------------------


def test_submit_proposal_rules(project: Project, freelancer: User, client_user: User) -> None:
    services.submit_proposal(
        project=project, freelancer=freelancer, cover_letter="hi", bid=Decimal(1)
    )
    with pytest.raises(services.BusinessRuleError, match="already"):
        services.submit_proposal(
            project=project, freelancer=freelancer, cover_letter="again", bid=Decimal(1)
        )
    with pytest.raises(services.BusinessRuleError, match="Only freelancers"):
        services.submit_proposal(
            project=project, freelancer=client_user, cover_letter="x", bid=Decimal(1)
        )


def test_accept_proposal_rejects_others(project: Project, freelancer: User) -> None:
    other = User.objects.create_user("grace", "grace@example.com", "pw-12345!")
    winner = services.submit_proposal(
        project=project, freelancer=freelancer, cover_letter="a", bid=Decimal(100)
    )
    loser = services.submit_proposal(
        project=project, freelancer=other, cover_letter="b", bid=Decimal(90)
    )
    services.accept_proposal(proposal=winner, by=project.client)
    loser.refresh_from_db()
    project.refresh_from_db()
    assert loser.status == Proposal.Status.REJECTED
    assert project.status == Project.Status.IN_PROGRESS
    with pytest.raises(services.BusinessRuleError):
        services.accept_proposal(proposal=loser, by=project.client)


def test_only_owner_can_accept(project: Project, freelancer: User) -> None:
    proposal = services.submit_proposal(
        project=project, freelancer=freelancer, cover_letter="a", bid=Decimal(1)
    )
    with pytest.raises(services.BusinessRuleError, match="owner"):
        services.accept_proposal(proposal=proposal, by=freelancer)


# --- HTML views ---------------------------------------------------------------


def test_project_list_page(client: Client, project: Project) -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert b"Build a REST API" in response.content


def test_project_detail_404(client: Client) -> None:
    assert client.get("/projects/999/").status_code == 404


def test_create_view_requires_client_role(
    client: Client, freelancer: User, client_user: User
) -> None:
    client.force_login(freelancer)
    assert client.get("/projects/new/").status_code == 403
    client.force_login(client_user)
    response = client.post(
        "/projects/new/", {"title": "Design a logo", "description": "svg", "budget": "50"}
    )
    assert response.status_code == 302
    assert Project.objects.filter(title="Design a logo", client=client_user).exists()


# --- REST API -----------------------------------------------------------------


def test_api_list_is_public_and_paginated(api: APIClient, project: Project) -> None:
    data = api.get("/api/v1/projects/").json()
    assert data["count"] == 1
    assert data["results"][0]["skills"] == ["django"]


def test_api_search(api: APIClient, project: Project) -> None:
    assert api.get("/api/v1/projects/?search=django").json()["count"] == 1
    assert api.get("/api/v1/projects/?search=nothing").json()["count"] == 0


def test_api_create_requires_auth_and_client_role(
    api: APIClient, client_user: User, freelancer: User
) -> None:
    payload = {"title": "Mobile app", "description": "Flutter", "budget": "900"}
    assert api.post("/api/v1/projects/", payload).status_code == 401
    api.force_authenticate(freelancer)
    assert api.post("/api/v1/projects/", payload).status_code == 403
    api.force_authenticate(client_user)
    response = api.post("/api/v1/projects/", payload)
    assert response.status_code == 201
    assert response.json()["client"] == "ada"


def test_api_validation_error(api: APIClient, client_user: User) -> None:
    api.force_authenticate(client_user)
    response = api.post("/api/v1/projects/", {"title": "x", "description": "d", "budget": "0"})
    assert response.status_code == 400
    assert set(response.json()) == {"title", "budget"}


def test_api_only_owner_can_update(api: APIClient, project: Project) -> None:
    intruder = User.objects.create_user("eve", "eve@example.com", "pw", role=User.Role.CLIENT)
    api.force_authenticate(intruder)
    assert api.patch(f"/api/v1/projects/{project.pk}/", {"budget": "1"}).status_code == 403


def test_api_proposal_flow(api: APIClient, project: Project, freelancer: User) -> None:
    api.force_authenticate(freelancer)
    url = f"/api/v1/projects/{project.pk}/proposals/"
    created = api.post(url, {"cover_letter": "I can do it", "bid": "450"})
    assert created.status_code == 201
    assert api.post(url, {"cover_letter": "again", "bid": "1"}).status_code == 400
    assert api.get(url).status_code == 403  # only the owner sees proposals

    api.force_authenticate(project.client)
    assert len(api.get(url).json()) == 1
    accepted = api.post(f"/api/v1/proposals/{created.json()['id']}/accept/")
    assert accepted.json()["status"] == "ACCEPTED"


def test_token_auth(api: APIClient, freelancer: User) -> None:
    token = api.post("/api/v1/auth/token/", {"username": "linus", "password": "pw-12345!"})
    assert token.status_code == 200
    api.credentials(HTTP_AUTHORIZATION=f"Token {token.json()['token']}")
    assert api.get("/api/v1/projects/").status_code == 200
