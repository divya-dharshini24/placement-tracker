from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Application

User = get_user_model()


def make_app(owner, **kwargs):
    data = {"company": "Acme", "role": "Analyst", "status": Application.Status.APPLIED}
    data.update(kwargs)
    return Application.objects.create(owner=owner, **data)


class BaseTestCase(TestCase):
    def setUp(self):
        self.alice = User.objects.create_user("alice", password="pass12345")
        self.bob = User.objects.create_user("bob", password="pass12345")
        self.client.login(username="alice", password="pass12345")


class LoginRequiredTests(TestCase):
    def test_pages_redirect_when_logged_out(self):
        for name in ["dashboard", "application_list", "add_application"]:
            response = self.client.get(reverse(name))
            self.assertRedirects(
                response,
                f"{reverse('login')}?next={reverse(name)}",
                fetch_redirect_response=False,
            )


class PrivacyTests(BaseTestCase):
    def test_list_shows_only_own_applications(self):
        make_app(self.alice, company="AliceCorp")
        make_app(self.bob, company="BobCorp")
        response = self.client.get(reverse("application_list"))
        self.assertContains(response, "AliceCorp")
        self.assertNotContains(response, "BobCorp")

    def test_cannot_edit_another_students_application(self):
        app = make_app(self.bob)
        response = self.client.get(reverse("edit_application", args=[app.pk]))
        self.assertEqual(response.status_code, 404)

    def test_cannot_delete_another_students_application(self):
        app = make_app(self.bob)
        response = self.client.post(reverse("delete_application", args=[app.pk]))
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Application.objects.filter(pk=app.pk).exists())

    def test_dashboard_counts_ignore_other_students(self):
        make_app(self.alice)
        make_app(self.bob)
        make_app(self.bob)
        response = self.client.get(reverse("dashboard"))
        applied = [s for s in response.context["status_counts"] if s["label"] == "Applied"][0]
        self.assertEqual(applied["count"], 1)


class DashboardTests(BaseTestCase):
    def test_status_counts(self):
        make_app(self.alice, status=Application.Status.APPLIED)
        make_app(self.alice, status=Application.Status.APPLIED)
        make_app(self.alice, status=Application.Status.INTERVIEW)
        response = self.client.get(reverse("dashboard"))
        counts = {s["label"]: s["count"] for s in response.context["status_counts"]}
        self.assertEqual(counts["Applied"], 2)
        self.assertEqual(counts["Interview"], 1)
        self.assertEqual(counts["Offer"], 0)

    def test_upcoming_deadlines_sorted_and_future_only(self):
        today = timezone.localdate()
        later = make_app(self.alice, company="Later", deadline_date=today + timedelta(days=10))
        soon = make_app(self.alice, company="Soon", deadline_date=today + timedelta(days=2))
        make_app(self.alice, company="Past", deadline_date=today - timedelta(days=1))
        make_app(self.alice, company="NoDate")
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(list(response.context["upcoming"]), [soon, later])

    def test_stale_applications_after_seven_days(self):
        old = make_app(self.alice, company="Old")
        fresh = make_app(self.alice, company="Fresh")
        Application.objects.filter(pk=old.pk).update(
            last_updated=timezone.now() - timedelta(days=8)
        )
        response = self.client.get(reverse("dashboard"))
        stale = list(response.context["stale"])
        self.assertIn(old, stale)
        self.assertNotIn(fresh, stale)

    def test_finished_applications_are_not_stale(self):
        offer = make_app(self.alice, status=Application.Status.OFFER)
        Application.objects.filter(pk=offer.pk).update(
            last_updated=timezone.now() - timedelta(days=30)
        )
        response = self.client.get(reverse("dashboard"))
        self.assertNotIn(offer, list(response.context["stale"]))


class ActionTests(BaseTestCase):
    def form_data(self, **kwargs):
        data = {
            "company": "NewCo",
            "role": "Developer",
            "status": "applied",
            "job_url": "",
            "notes": "",
        }
        data.update(kwargs)
        return data

    def test_add_application_sets_owner(self):
        response = self.client.post(reverse("add_application"), self.form_data())
        self.assertRedirects(response, reverse("application_list"))
        app = Application.objects.get(company="NewCo")
        self.assertEqual(app.owner, self.alice)

    def test_add_requires_company_and_role(self):
        response = self.client.post(
            reverse("add_application"), self.form_data(company="", role="")
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Application.objects.count(), 0)

    def test_deadline_label_without_date_is_rejected(self):
        response = self.client.post(
            reverse("add_application"), self.form_data(deadline_label="coding test")
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Application.objects.count(), 0)

    def test_edit_changes_status_and_last_updated(self):
        app = make_app(self.alice)
        Application.objects.filter(pk=app.pk).update(
            last_updated=timezone.now() - timedelta(days=10)
        )
        response = self.client.post(
            reverse("edit_application", args=[app.pk]),
            self.form_data(company="Acme", role="Analyst", status="interview"),
        )
        self.assertRedirects(response, reverse("application_list"))
        app.refresh_from_db()
        self.assertEqual(app.status, "interview")
        self.assertGreater(app.last_updated, timezone.now() - timedelta(days=1))

    def test_delete_application(self):
        app = make_app(self.alice)
        response = self.client.post(reverse("delete_application", args=[app.pk]))
        self.assertRedirects(response, reverse("application_list"))
        self.assertFalse(Application.objects.filter(pk=app.pk).exists())

    def test_delete_page_asks_for_confirmation(self):
        app = make_app(self.alice)
        response = self.client.get(reverse("delete_application", args=[app.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Application.objects.filter(pk=app.pk).exists())

    def test_filter_by_status(self):
        make_app(self.alice, company="AppliedCo", status=Application.Status.APPLIED)
        make_app(self.alice, company="InterviewCo", status=Application.Status.INTERVIEW)
        response = self.client.get(reverse("application_list"), {"status": "interview"})
        self.assertContains(response, "InterviewCo")
        self.assertNotContains(response, "AppliedCo")

    def test_invalid_filter_shows_everything(self):
        make_app(self.alice, company="AppliedCo")
        response = self.client.get(reverse("application_list"), {"status": "nonsense"})
        self.assertContains(response, "AppliedCo")