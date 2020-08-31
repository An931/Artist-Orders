from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, TemplateView
from django.views.generic.base import View

__all__ = (
    'HomeView',
    'ListSearchView',
    'BaseView',
)


class HomeView(TemplateView):
    """View for home page."""

    template_name = 'core/home.html'


class ListSearchView(ListView):
    """Base view for views with search functionality."""

    def get_queryset(self):
        """Return filtered by search value queryset."""
        qs = super().get_queryset()
        search_value = self.request.GET.get('search_box')

        if search_value is not None:
            qs = qs.search_by(search_value)

        return qs


class BaseView(LoginRequiredMixin, View):
    """Override get_queryset to return only available for user objects."""

    def get_queryset(self):
        """Return only available for user objects."""
        queryset = super().get_queryset()
        return queryset.available_for_user(self.request.user)
