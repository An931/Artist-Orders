from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import DeleteView, DetailView, FormView, UpdateView

from apps.core.views import BaseView, ListSearchView
from apps.files.models import File
from apps.masterpieces.models import Masterpiece
from apps.users.models import User

from ..orders.models import Order
from .forms import MasterpieceForm

__all__ = (
    'MasterpiecesList',
    'MasterpieceDetailView',
)


class MasterpiecesList(LoginRequiredMixin, ListSearchView):
    """View to see list of visible artists` masterpieces."""

    template_name = 'masterpieces/list.html'
    context_object_name = 'masterpieces'
    queryset = Masterpiece.objects.prefetch_related('tags', )
    paginate_by = 10

    def get_queryset(self):
        """Return all available authors` masterpieces."""
        queryset = super().get_queryset()
        user = self.request.user
        if 'artist_pk' in self.kwargs:
            self.artist = get_object_or_404(
                User, id=self.kwargs['artist_pk'], role=User.ROLES.ARTIST
            )
            return queryset.filter(artist=self.artist).all_visible()
        return queryset.filter(artist=user)

    def get_context_data(self, **kwargs):
        """Add an artist to context."""
        context = super().get_context_data(**kwargs)
        if 'artist_pk' in self.kwargs:
            context['artist'] = self.artist
        return context


class MasterpieceDetailView(BaseView, DetailView):
    """View to see the full masterpiece information."""

    template_name = 'masterpieces/detail.html'
    queryset = Masterpiece.objects.select_related('artist')
    context_object_name = 'masterpiece'


class MasterpieceCreationView(LoginRequiredMixin, FormView):
    """View for masterpiece creation."""

    template_name = "masterpieces/creation.html"
    form_class = MasterpieceForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        form.instance.artist = request.user
        if 'order_pk' in kwargs:
            order_id = kwargs['order_pk']
            order = Order.objects.get(id=order_id)
            form.instance.order = order

        if form.is_valid():
            files = request.FILES.getlist('files')
            masterpiece = form.save()
            for file in files:
                f = File.objects.create(link=file)
                masterpiece.files.add(f)
            return redirect(f'/masterpieces/{masterpiece.id}')
        return render(request, self.template_name, {'form': form})


class MasterpieceActionBaseView(BaseView, DetailView):
    """Base view for actions with masterpiece."""

    queryset = Masterpiece.objects

    def get_success_url(self):
        """Return urt to masterpiece detail page."""
        success_url = getattr(self, 'success_url', None)
        if success_url:
            return success_url
        masterpiece = self.get_object()
        return reverse_lazy(
            'masterpieces:masterpiece-detail',
            kwargs={'pk': masterpiece.id}
        )


class MasterpieceAcceptView(MasterpieceActionBaseView, UpdateView):
    """View to accept masterpiece by customer.

    Set customers` rate.
    """

    fields = ['customer_rate', ]
    template_name_suffix = '_accept_form'


class MasterpieceDeclineView(MasterpieceActionBaseView, UpdateView):
    """View to decline masterpiece by customer.

    Set customers` decline message.
    """

    fields = ['decline_message', ]
    template_name_suffix = '_decline_form'


class MasterpieceOwnerView(MasterpieceActionBaseView):
    """Override get_queryset to return all artists masterpieces."""

    def get_queryset(self):
        """Return all artists` masterpieces."""
        super().get_queryset()
        user = self.request.user
        return Masterpiece.objects.filter(artist=user)


class MasterpieceUpdateView(MasterpieceOwnerView, UpdateView):
    """View to update masterpiece by artist."""

    template_name_suffix = '_update_form'
    form_class = MasterpieceForm


class MasterpieceDeleteView(MasterpieceOwnerView, DeleteView):
    """View to delete masterpiece by artist."""

    success_url = reverse_lazy('masterpieces:masterpiece-list')
