from django.contrib import admin

from apps.orders.models import Order

__all__ = (
    'OrderAdmin',
)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Order admin.

    Admin class definitions for ``Order`` model.
    """

    search_fields = (
        'created_by__email',
        'created_by__first_name',
        'created_by__last_name',
        'title',
        'tags__title',
    )
    list_display = (
        'id',
        'created_by',
        'title',
        'created_at',
        'complete_to',
        'completed_at',
    )
    list_display_links = (
        'created_by',
        'title',
    )
    list_filter = (
        'created_at',
    )
    readonly_fields = (
        'created_at',
        'updated_at',
        'completed_at',
    )
    autocomplete_fields = (
        'tags',
        'created_by',
        'files',
        'offer',
    )
