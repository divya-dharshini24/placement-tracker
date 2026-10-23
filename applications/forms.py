from django import forms

from .models import Application


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = [
            "company",
            "role",
            "status",
            "applied_date",
            "deadline_date",
            "deadline_label",
            "job_url",
            "notes",
        ]
        widgets = {
            "applied_date": forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
            "deadline_date": forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        }