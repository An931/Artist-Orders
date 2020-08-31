from django.contrib import admin, messages
from django_object_actions import DjangoObjectActions

from apps.offers.models import Offer

__all__ = (
    'OfferAdmin',
)


@admin.register(Offer)
class OfferAdmin(DjangoObjectActions, admin.ModelAdmin):
    """Offer admin.

    Admin class definitions for ``Offer`` model.
    """

    search_fields = (
        'order__title',
        'artist__email',
        'artist__first_name',
        'artist__last_name',
    )
    list_display = (
        'id',
        'order',
        'artist',
        'fee',
        'created_at',
        'declined_at',
        'accepted_at',
        'changes_requested',
    )
    list_display_links = ('order',)
    list_filter = (
        'created_at',
    )
    readonly_fields = (
        'created_at',
        'updated_at',
        'declined_at',
        'accepted_at',
        'changes_requested',
    )
    autocomplete_fields = (
        'order',
        'artist',
    )
    change_actions = ['accept', 'decline', 'request_changes']

    def _check_change_ability(self, request, obj, action):
        """Check if offer can be changed and create message error if not.

        action can be any of these (accept, decline, change)
        """
        if obj.declined_at and action != 'decline':
            messages.error(request, f'Declined offer can not be {action}ed.')
        elif obj.accepted_at and action != 'accept':
            messages.error(request, f'Accepted offer can not be {action}ed.')
        elif ((obj.accepted_at and action == 'accept') or
              (obj.declined_at and action == 'decline')):
            messages.error(request, f'Offer is already {action}ed.')
        else:
            return True

    def accept(self, request, obj):
        """Accept the offer."""
        if not self._check_change_ability(request, obj, 'accept'):
            return
        obj.accept()
        messages.success(request, f'Offer from {obj.artist} accepted.')

    def decline(self, request, obj):
        """Decline the offer."""
        if not self._check_change_ability(request, obj, 'decline'):
            return
        obj.decline()
        messages.success(request, f'Offer from {obj.artist} declined.')

    def request_changes(self, request, obj):
        """Request change of the offer."""
        if not self._check_change_ability(request, obj, 'change'):
            return
        obj.request_changes()
        messages.success(request,
                         f'Changes requested to offer from {obj.artist}.')
