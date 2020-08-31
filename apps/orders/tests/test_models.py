from django.test import TestCase

from apps.orders.factories import OrderFactory
from apps.orders.models import Order
from apps.users.factories import UserFactory
from apps.users.models import User


class OrderModelTest(TestCase):
    """Tests for Order model."""

    @classmethod
    def setUpTestData(cls):
        """Create test order."""
        cls.user = UserFactory()
        cls.order = OrderFactory(created_by=cls.user)
        return super().setUpTestData()

    def test_has_user(self):
        """Order info should be created by user."""
        self.assertEqual(self.order.created_by, self.user)

    def test_delete_if_user_deleted(self):
        """Order info should be deleted if user was deleted."""
        User.objects.get().delete()
        with self.assertRaises(Order.DoesNotExist):
            Order.objects.get()
