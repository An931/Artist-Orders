from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import DeleteView, DetailView, FormView, UpdateView

from apps.core.views import BaseView, ListSearchView
from apps.offers.models import Offer
from apps.orders.models import Order
from . import tasks

from .forms import OfferForm

__all__ = (
    'OfferList',
    'OfferDeleteView',
    'OfferUpdateView',
    'OfferAcceptView',
    'OfferDeclineView',
    'OfferRequestChangesView',
    'OfferSendingView',
)


class OfferList(LoginRequiredMixin, ListSearchView):
    """View for list all available offers."""

    paginate_by = 10
    queryset = Offer.objects
    template_name = 'offers/list.html'
    context_object_name = 'offers'
    order = None

    def get(self, request, *args, **kwargs):
        """Add order attribute to class."""
        if 'order_pk' in self.kwargs:
            user = self.request.user
            self.order = get_object_or_404(
                Order, id=self.kwargs['order_pk'], created_by=user
            )
        return super().get(self, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Add order to context."""
        context = super().get_context_data(**kwargs)
        if self.order:
            context['order'] = self.order
        return context

    def get_queryset(self):
        """Return only artists` offers or customer orders` offers."""
        queryset = super().get_queryset()
        if self.order:
            return queryset.filter(
                order=self.order, declined_at__isnull=True
            ).select_related('artist')
        user = self.request.user
        return queryset.all_visible_for_artist(user).select_related('order')


class OfferDeleteView(BaseView, DeleteView):
    """View to delete an offer."""

    model = Offer
    success_url = reverse_lazy('offers:offers-list')


class OfferUpdateView(BaseView, UpdateView):
    """View to update offers` fee."""

    queryset = Offer.objects.all_available()
    fields = ['fee', ]
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('offers:offers-list')


class OfferActionBaseView(BaseView, DetailView):
    """Base view for action views.

    Provide get method which call `action` of offer object
    and redirect to `success_url`.
    """

    queryset = Offer.objects.all_available()

    def __init__(self, **kwargs):
        """Check if `action` and `success_url` attributes are set."""
        cls = type(self)
        if not getattr(cls, 'action', None):
            raise ValueError('No action to call. Provide an action.')
        if (not getattr(cls, 'success_url', None) and
                not getattr(cls, 'get_success_url', None)):
            raise ValueError('No URL to redirect to. Provide a success_url.')
        super().__init__(**kwargs)

    def get(self, request, *args, **kwargs):
        """Call `action` of offer object and redirect to `success_url`."""
        self.offer = self.get_object()
        success_url = self.get_success_url()
        action = getattr(self.offer, self.action)
        action()
        return redirect(success_url)

    def get_success_url(self):
        """Return url to redirect in case of success."""
        return self.success_url


class OfferAcceptView(OfferActionBaseView):
    """View to accept an offer."""

    action = 'accept'

    def get_success_url(self):
        """Return url to an order."""
        return reverse_lazy(
            'orders:order-detail', kwargs={'pk': self.offer.order.id}
        )


class OfferDeclineView(OfferActionBaseView):
    """View to decline an offer."""

    action = 'decline'

    def get_success_url(self):
        """Return url to orders` offers list."""
        return reverse_lazy(
            'offers:order-offers-list',
            kwargs={'order_pk': self.offer.order.id}
        )


class OfferRequestChangesView(OfferActionBaseView):
    """View to request update offers` fee."""

    action = 'request_changes'

    def get_success_url(self):
        """Return url to orders` offers list."""
        return reverse_lazy(
            'offers:order-offers-list',
            kwargs={'order_pk': self.offer.order.id}
        )


class OfferSendingView(LoginRequiredMixin, FormView):
    """View for offer sending."""

    template_name = 'offers/offer_sending.html'
    form_class = OfferForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        form.instance.artist = request.user
        order = Order.objects.filter(id=kwargs['order_id']).first()
        form.instance.order = order
        if form.is_valid():
            form.save()
            # tasks.send_offer_task.delay(order.created_by.email)
            # todo
            tasks.send_offer_task.delay('art-orders@mail.ru')
            return redirect('orders:order-list')
        return render(request, self.template_name, {'form': form})
