from django.test import TestCase

from apps.offers.factories import OfferFactory
from apps.orders.factories import OrderFactory
from apps.users.factories import ArtistFactory, CustomerFactory


class OfferModelTest(TestCase):
    """Tests for Offer model."""

    @classmethod
    def setUpTestData(cls):
        """Create test offer."""
        cls.customer = CustomerFactory()
        cls.artist = ArtistFactory()
        cls.order = OrderFactory(created_by=cls.customer)
        cls.offer = OfferFactory(
            order=cls.order, artist=cls.artist
        )
        return super().setUpTestData()

    def test_has_artist(self):
        """Offer should be created by artist."""
        self.assertEqual(self.offer.artist, self.artist)

    def test_has(self):
        """Offer should have order information."""
        self.assertEqual(self.offer.order, self.order)
