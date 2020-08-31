import factory.fuzzy
from django.utils import timezone

from ..orders.factories import OrderFactory
from ..orders.models import Order
from ..users.factories import ArtistFactory, CustomerFactory
from . import models


class OfferFactory(factory.django.DjangoModelFactory):
    """Factory for Offer model."""

    order = factory.SubFactory(OrderFactory)
    artist = factory.SubFactory(ArtistFactory)
    fee = factory.fuzzy.FuzzyDecimal(low=100, high=999999)

    class Meta:
        model = models.Offer


class CompletedOrderFactory(factory.django.DjangoModelFactory):
    """Factory for completed Order model."""

    created_by = factory.SubFactory(CustomerFactory)
    offer = factory.SubFactory(
        OfferFactory,
        accepted_at=timezone.now() + timezone.timedelta(seconds=3)
    )
    title = factory.Faker('sentence')
    description = factory.Faker('sentence', nb_words=50)
    complete_to = factory.fuzzy.FuzzyDateTime(
        start_dt=timezone.now() + timezone.timedelta(days=1),
        end_dt=timezone.now() + timezone.timedelta(days=5)
    )
    completed_at = timezone.now()

    class Meta:
        model = Order
