import factory.fuzzy

from . import models
from .models import User

__all__ = (
    'UserFactory',
    'ArtistFactory',
    'CustomerFactory',
)


class UserFactory(factory.django.DjangoModelFactory):
    """Factory for User model."""

    email = factory.Faker('email')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    phone_number = factory.fuzzy.FuzzyText(length=12)

    class Meta:
        model = models.User


class ArtistFactory(UserFactory):
    """Factory for User artist model."""

    role = User.ROLES.ARTIST

    class Meta:
        model = models.User


class CustomerFactory(UserFactory):
    """Factory for User customer model."""

    role = User.ROLES.CUSTOMER

    class Meta:
        model = models.User
