from django.db import models

from apps.core.querysets import UserRoleRelatedQuerySetMixin

__all__ = (
    'OfferQuerySet',
)


class OfferQuerySet(UserRoleRelatedQuerySetMixin, models.QuerySet):
    """Custom queryset with custom filters."""

    def search_by(self, value: str):
        """Return only offers with the found search_value."""
        return self.filter(
            models.Q(artist__email__icontains=value) |
            models.Q(order__title__icontains=value) |
            models.Q(order__tags__title=value)
        ).distinct()

    def all_visible_for_artist(self, artist):
        """Return all created by artist and not accepted yet offers."""
        return self.filter(artist=artist, accepted_at__isnull=True)

    def all_available(self):
        """Return all open offers."""
        return self.filter(declined_at__isnull=True, accepted_at__isnull=True)

    def all_visible_for_customer(self, customer):
        """Return all offers for orders, created by a customer."""
        return self.filter(order__created_by=customer)
