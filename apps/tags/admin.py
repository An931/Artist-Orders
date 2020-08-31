from django.contrib import admin

from apps.tags.models import Tag

__all__ = (
    'TagAdmin',
)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Tag admin.

    Admin class definitions for ``Tag`` model.
    """

    search_fields = ('title',)
    list_display = (
        'id',
        'title',
    )
    list_display_links = ('title',)
