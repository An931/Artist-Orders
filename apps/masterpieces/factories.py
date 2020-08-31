import factory.fuzzy

from ..offers.factories import CompletedOrderFactory
from . import models


class MasterpieceFactory(factory.django.DjangoModelFactory):
    """Factory for Masterpiece model."""

    title = factory.Faker('sentence')
    description = factory.Faker('sentence')
    order = factory.SubFactory(CompletedOrderFactory)
    visible = factory.Faker('random_element', elements=[True, False])
    artist = factory.SelfAttribute('order.offer.artist')

    class Meta:
        model = models.Masterpiece
