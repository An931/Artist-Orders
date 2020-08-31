from django.contrib import admin

from .models import File

__all__ = (
    'FileAdmin',
)


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    """File admin.

    Admin class definitions for ``File`` model.
    """

    list_display = [
        'id',
        'link',
    ]
    list_display_links = [
        'id',
        'link',
    ]
    search_fields = [
        'link',
    ]
