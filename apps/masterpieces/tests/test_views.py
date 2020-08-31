from django.test import Client, TestCase

from apps.masterpieces.factories import MasterpieceFactory
from apps.users.factories import ArtistFactory, CustomerFactory

client = Client()


class MasterpieceViewsTest(TestCase):
    """Tests for masterpiece views."""

    @classmethod
    def setUpTestData(cls):
        """Create test data."""
        cls.artist = ArtistFactory()
        cls.customer = CustomerFactory()
        cls.visible_masterpiece = MasterpieceFactory(
            artist=cls.artist, visible=True
        )
        cls.invisible_masterpiece = MasterpieceFactory(
            artist=cls.artist, visible=False
        )
        return super().setUpTestData()

    def test_invisible_masterpiece_artist(self):
        """Check artists` rights to see different masterpieces.

        Artist can see all visible masterpieces.
        Artist can see his invisible masterpieces.
        Artist can`t see other invisible masterpieces.
        """
        client.force_login(self.artist)
        response = client.get(f'/masterpieces/{self.visible_masterpiece.id}/')
        self.assertEqual(200, response.status_code)
        response = client.get(
            f'/masterpieces/{self.invisible_masterpiece.id}/'
        )
        self.assertEqual(200, response.status_code)

        other_artist = ArtistFactory()
        other_visible_masterpiece = MasterpieceFactory(
            artist=other_artist, visible=True
        )
        response = client.get(
            f'/masterpieces/{other_visible_masterpiece.id}/')
        self.assertEqual(200, response.status_code)

        other_invisible_masterpiece = MasterpieceFactory(
            artist=other_artist, visible=False
        )
        response = client.get(
            f'/masterpieces/{other_invisible_masterpiece.id}/')
        self.assertEqual(404, response.status_code)

    def test_invisible_masterpiece_customer(self):
        """Check customers` rights to see different masterpieces.

        Customer can see all visible masterpieces.
        Customer can see invisible masterpieces created for his order.
        Customer can`t see other invisible masterpieces.
        """
        client.force_login(self.customer)
        response = client.get(f'/masterpieces/{self.visible_masterpiece.id}/')
        self.assertEqual(200, response.status_code)
        response = client.get(
            f'/masterpieces/{self.invisible_masterpiece.id}/'
        )
        self.assertEqual(404, response.status_code)
        customer_invisible_masterpiece = MasterpieceFactory(
            artist=self.artist, visible=False, order__created_by=self.customer
        )
        response = client.get(
            f'/masterpieces/{customer_invisible_masterpiece.id}/'
        )
        self.assertEqual(200, response.status_code)
