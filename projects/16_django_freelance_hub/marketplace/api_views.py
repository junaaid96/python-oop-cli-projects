"""DRF ViewSets. A router turns these into list/detail/custom-action URLs."""

from __future__ import annotations

from typing import Any

from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer

from . import services
from .models import Project, Proposal
from .permissions import IsClientOrReadOnly, IsOwnerOrReadOnly
from .serializers import ProjectSerializer, ProposalSerializer


class ProjectViewSet(viewsets.ModelViewSet):  # type: ignore[type-arg]
    serializer_class = ProjectSerializer
    permission_classes = (IsClientOrReadOnly, IsOwnerOrReadOnly)
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ("title", "description", "skills__name")
    ordering_fields = ("budget", "created_at")

    def get_queryset(self) -> Any:
        qs = Project.objects.with_related().with_proposal_count()
        status_param = self.request.query_params.get("status")
        if status_param:
            qs = qs.filter(status=status_param.upper())
        return qs

    def perform_create(self, serializer: BaseSerializer[Project]) -> None:
        serializer.save(client=self.request.user)

    @action(detail=True, methods=["get", "post"], permission_classes=[IsAuthenticated])
    def proposals(self, request: Request, pk: str | None = None) -> Response:
        project = self.get_object()
        if request.method == "GET":
            if project.client_id != request.user.pk:
                return Response(status=status.HTTP_403_FORBIDDEN)
            qs = project.proposals.select_related("freelancer")
            return Response(ProposalSerializer(qs, many=True).data)
        serializer = ProposalSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            proposal = services.submit_proposal(
                project=project,
                freelancer=request.user,  # type: ignore[arg-type]
                cover_letter=serializer.validated_data["cover_letter"],
                bid=serializer.validated_data["bid"],
            )
        except services.BusinessRuleError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(ProposalSerializer(proposal).data, status=status.HTTP_201_CREATED)


class ProposalViewSet(viewsets.GenericViewSet):  # type: ignore[type-arg]
    permission_classes = (IsAuthenticated,)
    serializer_class = ProposalSerializer
    queryset = Proposal.objects.select_related("project")

    @action(detail=True, methods=["post"])
    def accept(self, request: Request, pk: str | None = None) -> Response:
        proposal = get_object_or_404(self.get_queryset(), pk=pk)
        try:
            services.accept_proposal(proposal=proposal, by=request.user)  # type: ignore[arg-type]
        except services.BusinessRuleError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(ProposalSerializer(proposal).data)
