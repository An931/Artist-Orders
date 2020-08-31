import factory.fuzzy
from django.utils import timezone

from ..users.factories import CustomerFactory
from . import models


class OrderFactory(factory.django.DjangoModelFactory):
    """Factory for Order model."""

    created_by = factory.SubFactory(CustomerFactory)
    title = factory.Faker('sentence')
    description = factory.Faker('sentence', nb_words=50)
    complete_to = factory.fuzzy.FuzzyDateTime(
        start_dt=timezone.now() + timezone.timedelta(days=1),
        end_dt=timezone.now() + timezone.timedelta(days=5)
    )

    class Meta:
        model = models.Order
