from apps.users.strings import ARTIST_ROLE


class UserRoleRelatedQuerySetMixin:
    """Provide method which call queryset method according to users role."""

    def available_for_user(self, user):
        """Call queryset filter method according to users role."""
        if user.role == ARTIST_ROLE:
            return self.all_visible_for_artist(user)
        return self.all_visible_for_customer(user)
