from django.contrib import admin

from .models import Masterpiece

__all__ = (
    'MasterpieceAdmin',
)


@admin.register(Masterpiece)
class MasterpieceAdmin(admin.ModelAdmin):
    """Masterpiece admin.

    Admin class definitions for ``Masterpiece`` model.
    """

    readonly_fields = [
        'created_at',
        'updated_at',
    ]
    list_display = [
        'id',
        'artist',
        'title',
        'order',
        'created_at',
        'visible',
        'customer_rate',
    ]
    list_display_links = [
        'id',
        'artist',
        'title',
    ]
    autocomplete_fields = [
        'artist',
        'order',
        'files',
        'tags',
    ]
    list_filter = [
        'created_at',
    ]
    search_fields = [
        'title',
        'description',
        'artist__email',
    ]
