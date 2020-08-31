from django.contrib import admin

from apps.reports.models import MasterpieceReport, OrderReport, UserReport

__all__ = (
    'UserReportAdmin',
    'OrderReportAdmin',
    'MasterpieceReportAdmin',
)


@admin.register(UserReport)
class UserReportAdmin(admin.ModelAdmin):
    """User report admin.

    Admin class definitions for ``UserReport`` model.
    """

    search_fields = (
        'created_by__email',
        'user__email',
    )
    list_display = (
        'id',
        'created_by',
        'user',
        'created_at',
    )
    list_display_links = (
        'created_by',
    )
    list_filter = (
        'created_at',
    )
    autocomplete_fields = (
        'created_by',
        'user',
    )


@admin.register(OrderReport)
class OrderReportAdmin(admin.ModelAdmin):
    """Order report admin.

    Admin class definitions for ``OrderReport`` model.
    """

    search_fields = (
        'created_by__email',
        'order__id',
        'order__title',
    )
    list_display = (
        'id',
        'created_by',
        'order',
        'created_at',
    )
    list_display_links = (
        'created_by',
    )
    list_filter = (
        'created_at',
    )
    autocomplete_fields = (
        'created_by',
        'order',
    )


@admin.register(MasterpieceReport)
class MasterpieceReportAdmin(admin.ModelAdmin):
    """Masterpiece report admin.

    Admin class definitions for ``MasterpieceReport`` model.
    """

    search_fields = (
        'created_by__email',
        'masterpiece__title',
        'masterpiece__artist__email',
    )
    list_display = (
        'id',
        'created_by',
        'masterpiece',
        'created_at',
    )
    list_display_links = (
        'created_by',
    )
    list_filter = (
        'created_at',
    )
    autocomplete_fields = (
        'created_by',
        'masterpiece',
    )
    readonly_fields = (
        'created_at',
    )
