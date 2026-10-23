from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, redirect, render
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
    """Placeholder: the real dashboard is built on Day 3."""
    return render(request, "applications/dashboard.html")
@login_required
def application_list(request):
    """Show only the logged-in student's applications."""
    applications = Application.objects.filter(owner=request.user).order_by("-last_updated")
    return render(request, "applications/application_list.html", {"applications": applications})


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