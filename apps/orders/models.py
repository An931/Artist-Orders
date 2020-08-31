from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from apps.orders.querysets import OrderQuerySet
from apps.users.models import User

__all__ = (
    'Order',
)


def one_day_hence():
    return timezone.now() + timezone.timedelta(days=1)


class Order(models.Model):
    """Order model.

    Attributes:
        created_by (User): User created order.
        title (str): Title of order.
        description (str): Order full description.
        complete_to (datetime): Date when order should be completed.
        created_at (datetime): Date when order was created.
        updated_at (datetime): Date when order was updated.
        completed_at (datetime): Date when order was completed.
        offer (Offer): Accepted offer on order.
    """

    created_by = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='created_orders',
        verbose_name=_('Created by'),
    )
    title = models.CharField(
        max_length=255,
        verbose_name=_('Title'),
    )
    description = models.TextField(
        verbose_name=_('Description'),
    )
    complete_to = models.DateTimeField(
        default=one_day_hence,
        verbose_name=_('Complete to'),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created at'),
    )
    updated_at = models.DateTimeField(
        null=True,
        blank=True,
        auto_now=True,
        verbose_name=_('Updated at'),
    )
    completed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Completed at'),
    )
    views = models.PositiveIntegerField(
        default=0,
        verbose_name=_('Views count'),
    )

    offer = models.OneToOneField(
        'offers.Offer',
        on_delete=models.SET_NULL,
        related_name='accepted_order',
        null=True,
        blank=True,
    )
    tags = models.ManyToManyField(
        'tags.Tag',
        blank=True,
        related_name='orders',
    )
    files = models.ManyToManyField(
        'files.File',
        blank=True,
        related_name='orders',
    )
    objects = OrderQuerySet.as_manager()

    class Meta:
        db_table = 'orders'
        ordering = ('-created_at',)
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    def __str__(self):
        return self.title

    def clean(self):
        """Check if data is valid."""
        if not self.created_by or self.created_by.role != User.ROLES.CUSTOMER:
            raise ValidationError(
                _('Order must be created by customer.')
            )
        if self.complete_to < timezone.now():
            raise ValidationError(
                _('Order can not be completed in the past.')
            )
        if (self.offer and self.completed_at
                and self.completed_at < self.offer.accepted_at):
            raise ValidationError(
                _('Order can not be completed before offer was accepted.')
            )
