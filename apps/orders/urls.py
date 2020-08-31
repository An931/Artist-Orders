from django.urls import path

import apps.orders.views as orders_views
from apps.offers.views import OfferList, OfferSendingView

urlpatterns = (
    path('', orders_views.OrderList.as_view(), name='order-list'),
    path(
        'create/',
        orders_views.OrderCreationView.as_view(),
        name='create-order'
    ),
    path(
        '<int:pk>/',
        orders_views.OrderDetailView.as_view(),
        name='order-detail'
    ),
    path(
        '<int:pk>/update/',
        orders_views.OrderUpdateView.as_view(),
        name='order-update'
    ),
    path(
        '<int:pk>/delete/',
        orders_views.OrderDeleteView.as_view(),
        name='order-delete'
    ),
    path(
        '<int:order_id>/offer', OfferSendingView.as_view(), name='send-offer'
    ),
    path('<int:order_id>/offers', OfferList.as_view(), name='offers-list'),
    path(
        'customer/<int:customer_pk>/',
        orders_views.OrderList.as_view(),
        name='customer-orders-list'
    ),
    path(
        'artist/<int:artist_pk>/',
        orders_views.OrderList.as_view(),
        name='artist-orders-list'
    ),
)
