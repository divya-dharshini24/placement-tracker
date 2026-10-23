from datetime import timedelta

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import ApplicationForm
from .models import Application


def signup(request):
    """Create an account with Django's built-in form, then log the student in."""
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})


@login_required
def dashboard(request):
    """Counts by status, upcoming deadlines, and applications with no update for 7+ days."""
    mine = Application.objects.filter(owner=request.user)

    # 1. Counts by status (every status is shown, even when the count is 0)
    counts = dict(mine.values_list("status").annotate(Count("id")))
    status_counts = [
        {"label": label, "count": counts.get(value, 0)}
        for value, label in Application.Status.choices
    ]

    # 2. Upcoming deadlines, soonest first
    today = timezone.localdate()
    upcoming = mine.filter(deadline_date__gte=today).order_by("deadline_date")

    # 3. No update for more than 7 days (finished applications are left out)
    cutoff = timezone.now() - timedelta(days=7)
    stale = (
        mine.filter(last_updated__lt=cutoff)
        .exclude(status__in=[Application.Status.OFFER, Application.Status.REJECTED])
        .order_by("last_updated")
    )

    return render(
        request,
        "applications/dashboard.html",
        {"status_counts": status_counts, "upcoming": upcoming, "stale": stale},
    )


@login_required
def application_list(request):
    """Show only the logged-in student's applications, optionally filtered by status."""
    applications = Application.objects.filter(owner=request.user).order_by("-last_updated")

    # Filter by status, e.g. /applications/?status=interview
    selected_status = request.GET.get("status", "")
    if selected_status in Application.Status.values:
        applications = applications.filter(status=selected_status)
    else:
        selected_status = ""

    return render(
        request,
        "applications/application_list.html",
        {
            "applications": applications,
            "statuses": Application.Status.choices,
            "selected_status": selected_status,
        },
    )


@login_required
def add_application(request):
    if request.method == "POST":
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.owner = request.user  # keeps each student's data separate
            application.save()
            return redirect("application_list")
    else:
        form = ApplicationForm()
    return render(
        request,
        "applications/application_form.html",
        {"form": form, "title": "Add application"},
    )


@login_required
def edit_application(request, pk):
    # owner=request.user means a student can't open someone else's application
    application = get_object_or_404(Application, pk=pk, owner=request.user)
    if request.method == "POST":
        form = ApplicationForm(request.POST, instance=application)
        if form.is_valid():
            form.save()  # last_updated changes automatically
            return redirect("application_list")
    else:
        form = ApplicationForm(instance=application)
    return render(
        request,
        "applications/application_form.html",
        {"form": form, "title": "Edit application"},
    )


@login_required
def delete_application(request, pk):
    application = get_object_or_404(Application, pk=pk, owner=request.user)
    if request.method == "POST":
        application.delete()
        return redirect("application_list")
    return render(
        request,
        "applications/application_confirm_delete.html",
        {"application": application},
    )