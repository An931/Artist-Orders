from django.db import models
from django.utils.translation import ugettext_lazy as _

__all__ = (
    'UserReport',
    'OrderReport',
    'MasterpieceReport',
)


class Report(models.Model):
    """Base report model.

    Attributes:
        created_by (User): User created report.
        description (str): Report description.
        created_at (datetime): Date when report was created.
    """

    created_by = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        verbose_name=_('Created by'),
    )
    description = models.TextField(
        verbose_name=_('Description'),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created at'),
    )

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.created_by)


class UserReport(Report):
    """User report model.

    Attributes:
        user (User): User on whom the report was created.
    """

    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='reports',
    )

    class Meta:
        db_table = 'user_reports'
        ordering = ('-created_at',)
        verbose_name = _('User report')
        verbose_name_plural = _('User reports')


class OrderReport(Report):
    """Order info report model.

    Attributes:
        order (Order): Order info on which the report was created.
    """

    order = models.ForeignKey(
        'orders.Order',
        on_delete=models.CASCADE,
        related_name='reports',
    )

    class Meta:
        db_table = 'order_reports'
        ordering = ('-created_at',)
        verbose_name = _('Order report')
        verbose_name_plural = _('Order reports')


class MasterpieceReport(Report):
    """Masterpiece report model.

    Attributes:
        masterpiece (Masterpiece): Masterpiece on which the report was created.
    """

    masterpiece = models.ForeignKey(
        'masterpieces.Masterpiece',
        on_delete=models.CASCADE,
        related_name='reports',
    )

    class Meta:
        db_table = 'masterpiece_reports'
        ordering = ('-created_at',)
        verbose_name = _('Masterpiece report')
        verbose_name_plural = _('Masterpiece reports')
