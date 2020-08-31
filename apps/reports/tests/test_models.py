from django.test import TestCase

from apps.reports.factories import UserReportFactory
from apps.reports.models import UserReport
from apps.users.factories import UserFactory
from apps.users.models import User


class UserReportModelTest(TestCase):
    """Tests for UserReport model."""

    @classmethod
    def setUpTestData(cls):
        """Create test report."""
        cls.user = UserFactory()
        cls.reported_user = UserFactory()
        cls.report = UserReportFactory(
            created_by=cls.user, user=cls.reported_user
        )
        return super().setUpTestData()

    def test_has_user(self):
        """Report should be created by user."""
        self.assertEqual(self.report.created_by, self.user)

    def test_delete_if_user_deleted(self):
        """Report should be deleted if user was deleted."""
        User.objects.get().delete()
        with self.assertRaises(UserReport.DoesNotExist):
            UserReport.objects.get()
