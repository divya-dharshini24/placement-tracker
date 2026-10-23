from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Application(models.Model):
    """One job application belonging to one student."""

    class Status(models.TextChoices):
        APPLIED = "applied", "Applied"
        TEST = "test", "Test"
        INTERVIEW = "interview", "Interview"
        OFFER = "offer", "Offer"
        REJECTED = "rejected", "Rejected"

    # Every application belongs to exactly one student (the logged-in user).
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="applications",
    )
    company = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    applied_date = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.APPLIED
    )
    job_url = models.URLField(blank=True)
    notes = models.TextField(blank=True)
    deadline_date = models.DateField(null=True, blank=True)
    deadline_label = models.CharField(max_length=100, blank=True)
    # auto_now updates this on every save, which powers the "stale" list later.
    last_updated = models.DateTimeField(auto_now=True)

    def clean(self):
        # A label such as "coding test" only makes sense with a date.
        if self.deadline_label and not self.deadline_date:
            raise ValidationError(
                {"deadline_label": "Enter a deadline date to use a deadline label."}
            )

    def __str__(self):
        return f"{self.role} at {self.company}"
