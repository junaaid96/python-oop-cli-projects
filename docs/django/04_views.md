# 04 · Views: FBV vs CBV

See [`marketplace/views.py`](../../projects/16_django_freelance_hub/marketplace/views.py) for one of each.

```python
def project_detail(request, pk):  # function-based view
    project = get_object_or_404(Project.objects.with_related(), pk=pk)
    return render(request, "marketplace/project_detail.html", {"project": project})


class ProjectListView(ListView):  # class-based (generic) view
    paginate_by = 10

    def get_queryset(self):
        return Project.objects.open().with_related()
```

| | Function-based | Class-based |
|---|---|---|
| Readability | explicit, top to bottom | logic spread over overridable hooks |
| Reuse | decorators, helper functions | inheritance and mixins |
| Best for | one-off or unusual pages | CRUD (`ListView`, `DetailView`, `CreateView`, `UpdateView`, `DeleteView`) |

Common hooks: `get_queryset`, `get_context_data`, `form_valid`, `get_success_url`, `dispatch`.

Access control: `@login_required` / `@permission_required` for FBVs; `LoginRequiredMixin`, `PermissionRequiredMixin`, `UserPassesTestMixin` for CBVs (mixins go **left** of the view class). Django 5.1+ also has `LoginRequiredMiddleware` to make every page private by default.

Async views: `async def view(request)` works under ASGI; use `await Model.objects.aget(...)`, `async for obj in qs`. Only worth it when the view waits on I/O (HTTP calls).

## Exercises
1. Rewrite `project_detail` as a `DetailView` and compare.
2. Add an `UpdateView` that only the project owner can open.
