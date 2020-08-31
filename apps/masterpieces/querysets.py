from django.db import models
from django.db.models import Q

from apps.core.querysets import UserRoleRelatedQuerySetMixin

__all__ = (
    'MasterpieceQuerySet',
)


class MasterpieceQuerySet(UserRoleRelatedQuerySetMixin, models.QuerySet):
    """Custom queryset with a custom filter."""

    def search_by(self, value: str):
        """Filter masterpieces by search_value."""
        return self.filter(
            models.Q(title__icontains=value)
            | models.Q(description__icontains=value)
            | models.Q(tags__title=value)
        ).distinct()

    def all_visible(self):
        """Return only visible masterpieces."""
        return self.filter(visible=True)

    def all_visible_for_customer(self, customer):
        """Return only visible for customer masterpieces."""
        return self.filter(Q(visible=True) | Q(order__created_by=customer))

    def all_visible_for_artist(self, artist):
        """Return only visible for artist masterpieces."""
        return self.filter(Q(visible=True) | Q(artist=artist))
