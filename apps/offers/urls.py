from django.urls import path

from . import views

urlpatterns = (
    path('', views.OfferList.as_view(), name='offers-list'),
    path(
        'order/<int:order_pk>',
        views.OfferList.as_view(),
        name='order-offers-list'
    ),
    path(
        '<int:pk>/delete', views.OfferDeleteView.as_view(), name='offer-delete'
    ),
    path(
        '<int:pk>/update', views.OfferUpdateView.as_view(), name='offer-update'
    ),
    path(
        '<int:pk>/accept', views.OfferAcceptView.as_view(), name='offer-accept'
    ),
    path(
        '<int:pk>/decline',
        views.OfferDeclineView.as_view(),
        name='offer-decline'
    ),
    path(
        '<int:pk>/require_changes',
        views.OfferRequestChangesView.as_view(),
        name='offer-request-changes'
    ),
)
