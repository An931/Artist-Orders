from django.db import models
from django.utils.translation import ugettext_lazy as _

__all__ = (
    'File',
)


class File(models.Model):
    """File model.

    Attributes:
        link (str): File link.
    """

    link = models.FileField(
        upload_to='upload_files/'
    )

    class Meta:
        db_table = 'files'
        verbose_name = _('File')
        verbose_name_plural = _('Files')

    def __str__(self):
        return str(self.link)
