from django.db import IntegrityError
from django.test import TestCase

from apps.users.factories import ArtistFactory, CustomerFactory, UserFactory
from apps.users.models import User


class UserModelTest(TestCase):
    """Tests for User model."""

    @classmethod
    def setUpTestData(cls):
        """Create test user."""
        cls.user = UserFactory()
        return super().setUpTestData()

    def test_email(self):
        """Each user should have an email address."""
        self.assertTrue(hasattr(self.user, 'email'))

    def test_email_uniqueness(self):
        """Email should be unique for each user."""
        with self.assertRaises(IntegrityError):
            User.objects.create(email=self.user.email)

    def test_str(self):
        """User string should be its email address."""
        self.assertEqual(str(self.user), self.user.email)

    def test_full_name(self):
        """User full name should be its last name and first name."""
        self.assertEqual(
            self.user.get_full_name(),
            f'{self.user.last_name} {self.user.first_name}'
        )

    def test_role_customer(self):
        """Customer should have correct role in uppercase."""
        user = CustomerFactory()
        self.assertEqual(user.role, User.ROLES.CUSTOMER)

    def test_role_artist(self):
        """Artist should have correct role in uppercase."""
        user = ArtistFactory()
        self.assertEqual(user.role, User.ROLES.ARTIST)
