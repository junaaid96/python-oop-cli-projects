# 06 · Forms

Forms parse, validate and render user input. See [`marketplace/forms.py`](../../projects/16_django_freelance_hub/marketplace/forms.py).

```python
class ProjectForm(forms.ModelForm[Project]):
    class Meta:
        model = Project
        fields = ("title", "description", "budget", "skills")  # always an allow-list

    def clean_title(self):  # field-level validation
        title = self.cleaned_data["title"].strip()
        if len(title) < 5:
            raise forms.ValidationError("Title must be at least 5 characters.")
        return title
```

Validation order: field `to_python` → field validators → `clean_<field>()` → `clean()` (cross-field) → model `full_clean()` for ModelForms.

The classic view pattern:
```python
form = ProjectForm(request.POST or None)
if request.method == "POST" and form.is_valid():
    project = form.save(commit=False)
    project.client = request.user
    project.save()
    form.save_m2m()
    return redirect("project-list")  # Post/Redirect/Get
return render(request, "form.html", {"form": form})
```

- Never use `fields = "__all__"` on public forms: new model fields would become editable (mass assignment).
- Every POST form needs `{% csrf_token %}`.
- Formsets edit many objects at once; `inlineformset_factory` for parent/children.

## Exercises
1. Add a `clean()` that rejects budgets under 50 when the skill list contains "django".
2. Build a proposal form with a formset.
