from statistics import mean
from urllib.parse import urljoin

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from apps.masterpieces.models import Masterpiece
from apps.users.managers import UserManager
from apps.users.strings import ARTIST_ROLE, CUSTOMER_ROLE

__all__ = (
    'User',
)


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model.

    Attributes:
        first_name (str): First name.
        last_name (str): Last, family name.
        email (str): E-mail, uses for authentication.
        is_active (bool): Can user log in to the system.
        is_staff (bool): Can user access to admin interface.
        date_joined (datetime): Date when the account was created.
        role (str): Role of user (artist or customer).
        phone_number (str): Phone number.

    Nested attributes:
        is_superuser (bool): The user can super access to admin UI.
        groups(Manager): The groups this user belongs to.
        user_permissions(Manager): Specified permissions for this user.
        last_login (datetime): Last date when user login to the system.
    """

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    ROLES = models.TextChoices('ROLES', (CUSTOMER_ROLE, ARTIST_ROLE))

    first_name = models.CharField(
        max_length=255,
        verbose_name=_('First name'),
    )
    last_name = models.CharField(
        max_length=255,
        verbose_name=_('Last name'),
    )
    email = models.EmailField(
        max_length=255,
        unique=True,
        verbose_name=_('Email'),
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Is active'),
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name=_('Is staff'),
        help_text=_('The user will have access to admin interface.'),
    )
    date_joined = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Date joined'),
    )
    role = models.CharField(
        max_length=255,
        choices=ROLES.choices,
        null=True,
        verbose_name=_('Role'),
        help_text=_('The user is artist or customer.'),
    )
    phone_number = PhoneNumberField(
        null=True,
        blank=True,
        verbose_name=_('Phone number'),
        help_text=_('Users phone number. '
                    'It has to be a phone number with country code.'),
    )
    objects = UserManager()

    class Meta:
        db_table = 'users'
        ordering = ('email',)
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        """Save user method.

        Save role field in uppercase.
        """
        if self.role:
            self.role = self.role.upper()
        super().save(*args, **kwargs)

    def get_full_name(self):
        """Return last name and first name of user."""
        full_name = '{first_name} {last_name}'.format(
            first_name=self.last_name,
            last_name=self.first_name,
        )

        return full_name.strip()

    def get_short_name(self):
        """Return first name of user."""
        return self.first_name

    def get_admin_change_url(self) -> str:
        """Get admin change URL.

        Build full url (host + path) to standard Django admin page for
        object like:

            https://api.sitename.com/admin/users/user/234/

        """
        assert self.id, "Instance must have an ID"

        return urljoin(
            settings.DJANGO_SITE_BASE_HOST,
            reverse('admin:users_user_change', args=(self.id,)),
        )

    @property
    def rating(self):
        """Return the user's rating for all orders completed by him."""
        feedbacks = Masterpiece.objects.filter(
            artist=self, customer_rate__isnull=False
        ).values_list('customer_rate', flat=True)
        if feedbacks:
            return round(mean(feedbacks), 2)

    @property
    def completed_orders_count(self):
        """Return count of completed by user orders."""
        return self.masterpieces.filter(order__isnull=False).count()
