from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from apps.offers.querysets import OfferQuerySet
from apps.users.models import User

__all__ = (
    'Offer',
)


class Offer(models.Model):
    """Offer model.

    Attributes:
        order (Order): Id of order information.
        artist (User): Author who made the offer.
        fee (decimal): Fee for which the artist is ready to fulfill the order.
        created_at (datetime): Date when offer was created.
        updated_at (datetime): Date when offer was updated.
        declined_at (datetime): Date when offer was declined.
        accepted_at (datetime): Date when offer was accepted.
        changes_requested (bool): If user requested changes of offer.
    """

    order = models.ForeignKey(
        'orders.Order',
        on_delete=models.CASCADE,
        related_name='offers',
        verbose_name=_('Order info'),
    )
    artist = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='offers',
        verbose_name=_('Artist'),
    )
    fee = models.DecimalField(
        max_digits=6,
        decimal_places=0,
        verbose_name=_('Fee'),
        validators=[MinValueValidator(0.0)],
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created at'),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Updated at'),
    )
    declined_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Declined at'),
    )
    accepted_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Accepted at'),
    )
    changes_requested = models.BooleanField(
        default=False,
        verbose_name=_('Changes requested')
    )

    objects = OfferQuerySet.as_manager()

    class Meta:
        db_table = 'offers'
        ordering = ('-created_at',)
        verbose_name = _('Offer')
        verbose_name_plural = _('Offers')
        unique_together = ('order', 'artist')

    def __str__(self):
        return str(self.order)

    def save(self, *args, **kwargs):
        """Save offer method.

        If offer fee was updated, field changes_requested changes to False.
        """
        original_offer = Offer.objects.filter(pk=self.pk).first()
        if not original_offer:
            return super().save(*args, **kwargs)

        if original_offer.fee != self.fee:
            self.changes_requested = False
        return super().save(*args, **kwargs)

    def clean(self):
        """Check if data is valid."""
        if not self.artist or self.artist.role != User.ROLES.ARTIST:
            raise ValidationError(
                _('Offer can be created only by artist.')
            )
        if self.order.offer:
            raise ValidationError(
                _('Offer can not be created on order with accepted offer.')
            )
        if self.accepted_at and self.accepted_at < self.created_at:
            raise ValidationError(
                _('Offer can not be accepted before created.')
            )
        if self.declined_at and self.declined_at < self.created_at:
            raise ValidationError(
                _('Offer can not be declined before created.')
            )
        if self.declined_at and self.accepted_at:
            raise ValidationError(
                _('Offer can not be both declined and accepted.')
            )
        if self.changes_requested:
            if self.accepted_at or self.declined_at:
                state = 'Accepted' if self.accepted_at else 'Declined'
                raise ValidationError(
                    _(f'{state} offer can not be changed.'))

        offer_exists = Offer.objects.filter(
            artist=self.artist,
            order=self.order
        ).exclude(id=self.id).exists()

        if offer_exists:
            raise ValidationError(_('This offer is already created.'))

    def request_changes(self):
        """Set field changes_requested to True."""
        self.changes_requested = True
        self.save()

    def accept(self):
        """Set accepted_at date, set offer to an order and decline others."""
        self.accepted_at = timezone.now()
        self.request_changes = False
        self.save()
        self.order.offer = self
        self.order.save()
        self.order.offers.exclude(id=self.id).update(
            declined_at=timezone.now()
        )

    def decline(self):
        """Set declined_at date."""
        self.declined_at = timezone.now()
        self.save()
