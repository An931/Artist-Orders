from django.db import models

from apps.core.querysets import UserRoleRelatedQuerySetMixin

__all__ = (
    'OrderQuerySet',
)


class OrderQuerySet(UserRoleRelatedQuerySetMixin, models.QuerySet):
    """Custom queryset with a custom filters."""

    def search_by(self, value: str):
        """Return only order infos with the found search_value."""
        return self.filter(
            models.Q(title__icontains=value) |
            models.Q(description__icontains=value) |
            models.Q(tags__title=value)
        ).distinct()

    def all_available(self):
        """Return all open orders."""
        return self.filter(offer__isnull=True)

    def all_visible_for_customer(self, customer):
        """Return all created by a customer orders."""
        return self.filter(created_by=customer)

    def all_visible_for_artist(self, artist):
        """Return all open or completed by artist orders."""
        return self.filter(
            models.Q(offer__isnull=True) |
            models.Q(offer__isnull=False, offer__artist=artist)
        )

    def all_accepted_for_artist(self, artist):
        """Return all orders for which artists` offer was accepted."""
        return self.filter(
            offer__isnull=False,
            offer__artist=artist,
            offer__accepted_at__isnull=False
        )
