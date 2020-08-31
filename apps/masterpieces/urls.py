from django.urls import path

from apps.masterpieces import views

urlpatterns = (
    path(
        '<int:pk>/',
        views.MasterpieceDetailView.as_view(),
        name='masterpiece-detail'
    ),
    path('', views.MasterpiecesList.as_view(), name='masterpiece-list'),
    path(
        'artist/<int:artist_pk>/',
        views.MasterpiecesList.as_view(),
        name='artist-masterpiece-list'
    ),
    path(
        'order/<int:order_pk>/create/',
        views.MasterpieceCreationView.as_view(),
        name='upload-masterpiece'
    ),
    path(
        'create/',
        views.MasterpieceCreationView.as_view(),
        name='create-masterpiece'
    ),
    path(
        '<int:pk>/accept/',
        views.MasterpieceAcceptView.as_view(),
        name='masterpiece-accept'
    ),
    path(
        '<int:pk>/decline/',
        views.MasterpieceDeclineView.as_view(),
        name='masterpiece-decline'
    ),
    path(
        '<int:pk>/update/',
        views.MasterpieceUpdateView.as_view(),
        name='masterpiece-update'
    ),
    path(
        '<int:pk>/delete/',
        views.MasterpieceDeleteView.as_view(),
        name='masterpiece-delete'
    ),
)
