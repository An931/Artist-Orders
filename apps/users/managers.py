from django.contrib.auth.models import BaseUserManager
from django.db.models import Q, QuerySet
from django.utils.translation import ugettext_lazy as _

from apps.users.strings import ARTIST_ROLE, CUSTOMER_ROLE

__all__ = (
    'UserManager',
)


class UserManager(BaseUserManager):
    """Custom user manager.

    The custom user manager needs instead base manager because we use
    ``email`` instead ``username`` for authentication.

    """

    def create_user(
            self, *,
            email: str,
            first_name: str,
            last_name: str,
            role: str = None,
            phone_number: str = None,
            password: str = None
    ):
        """Create user.

        Overridden base user manager method, customized for auth with email
        instead username.

        """
        if not email:
            raise ValueError(_('Users must have an email address!'))

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            role=role,
            phone_number=phone_number,
        )

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email: str, password: str):
        """Create superuser.

        Overridden base user manager method, customized for auth with email
        instead username.

        """
        user = self.create_user(
            email=email, password=password, first_name='', last_name=''
        )

        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user

    def update_user(self, id: int, **kwargs):
        """Update users attributes."""
        user = self.get(id=id)
        for attr, value in kwargs.items():
            if hasattr(user, attr):
                setattr(user, attr, value)
            else:
                raise ValueError(f'Unknown attribute {attr}')
        user.save()

    def delete_user(self, id: int):
        """Delete user."""
        self.get(id=id).delete()

    def get_queryset(self):
        """Return custom queryset."""
        return UserQuerySet(self.model)


class UserQuerySet(QuerySet):
    """Custom queryset with a custom filters."""

    def search_by(self, value: str):
        """Return queryset filtered by search value."""
        return self.filter(
            Q(first_name__icontains=value)
            | Q(last_name__icontains=value)
            | Q(email__icontains=value)
        ).distinct()

    def get_artists(self):
        """Return all users with role artist."""
        return self.filter(role=ARTIST_ROLE)

    def get_customers(self):
        """Return all users with role customer."""
        return self.filter(role=CUSTOMER_ROLE)
