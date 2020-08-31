from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from apps.masterpieces.querysets import MasterpieceQuerySet

__all__ = (
    'Masterpiece',
)

from apps.users.strings import ARTIST_ROLE


class Masterpiece(models.Model):
    """Masterpiece model.

    Attributes:
        artist (User): Author of masterpiece.
        title (str): Title of masterpiece.
        description (str): Description of masterpiece.
        created_at (datetime): Datetime when masterpiece was created.
        updated_at (datetime): Datetime when masterpiece was updated.
        customer_rate (int): Orders` customer rate.
        decline_message (str): Message with which masterpiece was declined.
        visible (bool): Is masterpiece visible to other users.
        order (Order): Order of masterpiece.
    """

    RATES_CHOICES = (
        (1, 'Very bad'),
        (2, 'Bad'),
        (3, 'Normal'),
        (4, 'Good'),
        (5, 'Very good')
    )
    artist = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='masterpieces',
        verbose_name=_('Artist'),
    )
    title = models.CharField(
        max_length=255,
        verbose_name=_('Title'),
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('Description'),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name=_('Created at'),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        editable=False,
        verbose_name=_('Updated at'),
    )
    customer_rate = models.IntegerField(
        null=True,
        choices=RATES_CHOICES,
        verbose_name=_('Customer rate')
    )
    decline_message = models.TextField(
        null=True,
        max_length=255,
        verbose_name=_('Decline message'),
    )
    visible = models.BooleanField(
        default=True,
        verbose_name=_('Visible'),
        help_text=_('Is masterpiece visible for other users.'),
    )
    order = models.OneToOneField(
        'orders.Order',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='masterpiece',
        verbose_name=_('Order'),
    )
    files = models.ManyToManyField(
        'files.File',
        blank=True,
        related_name='masterpieces',
    )
    tags = models.ManyToManyField(
        'tags.Tag',
        blank=True,
        related_name='masterpieces',
    )

    objects = MasterpieceQuerySet.as_manager()

    class Meta:
        db_table = 'masterpieces'
        ordering = ('-created_at',)
        verbose_name = _('Masterpiece')
        verbose_name_plural = _('Masterpieces')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Save masterpiece method.

        Set complete date to order if masterpiece was accepted.
        Remove decline_message if masterpiece was updated.
        """
        if not self.order:
            return super().save(*args, **kwargs)
        if self.customer_rate:
            self.decline_message = None
            self.order.completed_at = timezone.now()
            self.order.save()
        else:
            last_masterpiece = Masterpiece.objects.filter(pk=self.pk).first()
            if (last_masterpiece and
                    last_masterpiece.decline_message == self.decline_message):
                self.decline_message = None
        return super().save(*args, **kwargs)

    def clean(self):
        """Check if data is valid."""
        if self.artist.role != ARTIST_ROLE:
            raise ValidationError(
                _('Masterpiece must be created by artist.')
            )
        if self.order:
            if not self.order.offer:
                raise ValidationError(
                    _('Can`t create masterpiece to order '
                      'without accepted offer.')
                )
            if self.artist != self.order.offer.artist:
                raise ValidationError(
                    _('Can`t create masterpiece on order '
                      'from not accepted artist.')
                )
