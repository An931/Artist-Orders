from django.db import models
from django.utils.translation import ugettext_lazy as _

__all__ = (
    'Tag',
)


class Tag(models.Model):
    """Tag model.

    Attributes:
        title (str): Tag title.
    """

    title = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_('Title'),
    )

    class Meta:
        db_table = 'tags'
        ordering = ('title',)
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Save tag method.

        Save title in lower case.
        """
        self.title = self.title.lower()
        super().save(*args, **kwargs)
