import factory

from . import models


class TagFactory(factory.django.DjangoModelFactory):
    """Factory for Tag model."""

    title = factory.Faker('word')

    class Meta:
        model = models.Tag
