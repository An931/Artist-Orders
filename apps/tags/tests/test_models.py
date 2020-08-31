from django.db import IntegrityError
from django.test import TestCase

from apps.tags.factories import TagFactory
from apps.tags.models import Tag


class TagModelTest(TestCase):
    """Tests for Tag model."""

    @classmethod
    def setUpTestData(cls):
        """Create test tag."""
        cls.tag = TagFactory()
        return super().setUpTestData()

    def test_title_uniqueness(self):
        """Tag title should be unique."""
        with self.assertRaises(IntegrityError):
            Tag.objects.create(title=self.tag.title)
