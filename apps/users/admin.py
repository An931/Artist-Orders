from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _
from django_object_actions import DjangoObjectActions

from .models import User

__all__ = (
    'UserAdmin',
)


def deactivate(modeladmin, request, queryset):
    """Deactivate all users except superuser."""
    qs = queryset.exclude(is_superuser=True)
    qs.update(is_active=False)
    messages.success(request, f'Deactivated {qs.count()} user(s)')


@admin.register(User)
class UserAdmin(DjangoObjectActions, DjangoUserAdmin):
    """User admin.

    Admin class definitions for ``User`` model.

    """

    search_fields = (
        'first_name',
        'last_name',
        'email',
        'role',
    )
    list_display = (
        'id',
        'email',
        'role',
        'date_joined',
        'last_login',
        'is_active',
        'is_staff',
        'is_superuser',
    )
    list_display_links = ('email',)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2',),
        }),
        (_('Personal info'), {
            'fields': (
                'first_name',
                'last_name',
                'role',
                'phone_number',
            )
        })

    )
    fieldsets = (
        (None, {'fields': ('email', 'password',)}),
        (_('Personal info'), {
            'fields': (
                'first_name',
                'last_name',
                'role',
                'phone_number',
            )
        }),
        (_('Permissions'), {
            'classes': (
                'collapse',
            ),
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            )
        }),
        (_('Important dates'), {
            'fields': ('last_login', 'date_joined',)
        }),
    )
    readonly_fields = DjangoUserAdmin.readonly_fields + (
        'last_login',
        'date_joined',
    )
    list_filter = (
        'role',
        'is_active',
        'is_staff',
        'is_superuser',
    )
    ordering = ('email',)
    actions = [deactivate]
    change_actions = ['deactivate']

    def deactivate(self, request, obj):
        """Deactivate user if it is not superuser."""
        if obj.is_superuser:
            messages.error(request, 'Superuser can not be deactivated')
            return

        obj.is_active = False
        obj.save()
        messages.success(request, f'User {obj.get_full_name()} deactivated')
