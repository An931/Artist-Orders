from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView, UpdateView
from django.views.generic.base import View

from ..core.views import ListSearchView
from .forms import UserForm
from .models import User

__all__ = (
    'AccountsRegisterView',
    'ArtistsList',
)


class AccountsRegisterView(FormView):
    """View for registration."""

    template_name = "users/register.html"
    form_class = UserForm
    success_url = '/'

    def form_valid(self, form):
        """Save new user and login him."""
        password = form.cleaned_data['password']
        saved_user = User.objects.create_user(
            email=form.instance.email,
            password=password,
            first_name=form.instance.first_name,
            last_name=form.instance.first_name,
            role=form.instance.role,
            phone_number=form.instance.phone_number,
        )
        login(self.request, saved_user)
        return super().form_valid(form)


class ArtistsList(ListSearchView):
    """View for list all artists."""

    paginate_by = 10
    template_name = 'users/artists_list.html'
    context_object_name = 'artists'
    queryset = User.objects.all().get_artists().prefetch_related(
        'masterpieces',
    )


class UserProfileBaseView(LoginRequiredMixin, View):
    """Base view for user profile to leave only authorized user in queryset."""

    queryset = User.objects

    def get_queryset(self):
        """Leave only authorized user in queryset."""
        queryset = super().get_queryset()
        user = self.request.user
        return queryset.filter(id=user.id)


class UserDetailView(UserProfileBaseView, DetailView):
    """View to see users` profile."""

    template_name = 'users/profile_detail.html'


class UserUpdateView(UserProfileBaseView, UpdateView):
    """View to update users` profile."""

    model = User
    fields = ['last_name', 'first_name', 'phone_number', ]
    template_name_suffix = '_update_form'

    def get_success_url(self):
        """Return url for users` profile page."""
        return reverse_lazy(
            'users:user-detail',
            kwargs={'pk': self.kwargs['pk']}
        )
