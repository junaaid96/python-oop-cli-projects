"""HTML views: one function-based view and two class-based views, to compare."""

from __future__ import annotations

from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.forms import ModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from .forms import ProjectForm
from .models import Project


class ProjectListView(ListView):  # type: ignore[type-arg]
    template_name = "marketplace/project_list.html"
    paginate_by = 10

    def get_queryset(self) -> Any:
        return Project.objects.open().with_related().with_proposal_count()


def project_detail(request: HttpRequest, pk: int) -> HttpResponse:
    """Function-based view: explicit and easy to read for simple pages."""
    project = get_object_or_404(Project.objects.with_related(), pk=pk)
    return render(request, "marketplace/project_detail.html", {"project": project})


class ProjectCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):  # type: ignore[type-arg]
    form_class = ProjectForm
    template_name = "marketplace/project_form.html"
    success_url = reverse_lazy("project-list")

    def test_func(self) -> bool:
        return bool(getattr(self.request.user, "is_client", False))

    def form_valid(self, form: ModelForm[Any]) -> HttpResponse:
        form.instance.client = self.request.user
        return super().form_valid(form)
