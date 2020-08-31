import factory

from ..masterpieces.factories import MasterpieceFactory
from ..orders.factories import OrderFactory
from ..users.factories import UserFactory
from . import models


class UserReportFactory(factory.django.DjangoModelFactory):
    """Factory for UserReport model."""

    created_by = factory.SubFactory(UserFactory)
    user = factory.SubFactory(UserFactory)
    description = factory.Faker('sentence')

    class Meta:
        model = models.UserReport


class OrderReportFactory(factory.django.DjangoModelFactory):
    """Factory for OrderReport model."""

    created_by = factory.SubFactory(UserFactory)
    order = factory.SubFactory(OrderFactory)
    description = factory.Faker('sentence')

    class Meta:
        model = models.OrderReport


class MasterpieceReportFactory(factory.django.DjangoModelFactory):
    """Factory for MasterpieceReport model."""

    created_by = factory.SubFactory(UserFactory)
    masterpiece = factory.SubFactory(MasterpieceFactory)
    description = factory.Faker('sentence')

    class Meta:
        model = models.MasterpieceReport
