from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import generic

from apps.orders.models import Order

from ..core.views import BaseView, ListSearchView
from ..users.models import User
from .forms import OrderForm

__all__ = (
    'OrderList',
    'OrderDetailView',
    'OrderUpdateView',
    'OrderDeleteView',
    'OrderCreationView',
)

from ..users.strings import ARTIST_ROLE


class OrderList(LoginRequiredMixin, ListSearchView):
    """View for list all available orders."""

    paginate_by = 10
    template_name = 'orders/list.html'
    context_object_name = 'orders'
    queryset = Order.objects.order_by(
        F('completed_at').desc(nulls_last=False)
    ).select_related('masterpiece').prefetch_related('tags')

    def get_queryset(self):
        """Return visible orders according to users` role."""
        queryset = super().get_queryset()
        user = self.request.user
        if 'customer_pk' in self.kwargs:
            self.customer = get_object_or_404(
                User, id=self.kwargs['customer_pk'], role=User.ROLES.CUSTOMER
            )
            return queryset.all_visible_for_customer(
                self.customer
            ).all_available()

        if 'artist_pk' in self.kwargs:
            artist = get_object_or_404(
                User, id=self.kwargs['artist_pk'], role=User.ROLES.ARTIST
            )
            return queryset.all_accepted_for_artist(artist).select_related(
                'created_by'
            )

        if user.role == User.ROLES.ARTIST:
            return queryset.all_available().select_related('created_by')
        if user.role == User.ROLES.CUSTOMER:
            return queryset.all_visible_for_customer(user).select_related(
                'offer',
                'offer__artist',
            )
        return queryset

    def get_context_data(self, **kwargs):
        """Add a customer to context."""
        context = super().get_context_data(**kwargs)
        if 'customer_pk' in self.kwargs:
            context['customer'] = self.customer
        return context


class OrderCreationView(LoginRequiredMixin, generic.TemplateView):
    """View for order creation."""

    template_name = "orders/order_creation.html"
    form_class = OrderForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        form.instance.created_by = request.user
        if form.is_valid():
            form.save()
            return redirect('orders:order-detail', pk=form.instance.pk)

        return render(request, self.template_name, {'form': form})


class OrderDeleteView(BaseView, generic.DeleteView):
    """View to delete an order."""

    queryset = Order.objects.all_available()
    success_url = reverse_lazy('orders:order-list')


class OrderUpdateView(BaseView, generic.UpdateView):
    """View to update an order."""

    queryset = Order.objects.all_available()
    fields = ['title', 'description', 'complete_to', ]
    template_name_suffix = '_update_form'

    def get_success_url(self):
        """Return url for updated order."""
        return reverse_lazy(
            'orders:order-detail', kwargs={'pk': self.kwargs['pk']}
        )


class OrderDetailView(BaseView, generic.DetailView):
    """View to see the full order information."""

    template_name = 'orders/detail.html'
    queryset = Order.objects.select_related('created_by')
    context_object_name = 'order'

    def get_object(self):
        order = super().get_object()
        order.views += 1
        order.save()
        return order
