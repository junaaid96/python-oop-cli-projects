from django import forms

from .models import Project


class ProjectForm(forms.ModelForm[Project]):
    """ModelForm: fields, widgets and validation generated from the model."""

    class Meta:
        model = Project
        fields = ("title", "description", "budget", "skills")

    def clean_title(self) -> str:
        title: str = self.cleaned_data["title"].strip()
        if len(title) < 5:
            raise forms.ValidationError("Title must be at least 5 characters.")
        return title
