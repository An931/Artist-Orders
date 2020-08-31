from django.contrib.auth import views as auth_views
from django.urls import path

from apps.users import views

urlpatterns = (
    path(
        'accounts/login/',
        auth_views.LoginView.as_view(template_name='users/login.html'),
        name='login'
    ),
    path(
        'accounts/logout/',
        auth_views.LogoutView.as_view(),
        name='logout'
    ),
    path(
        'accounts/register/',
        views.AccountsRegisterView.as_view(),
        name='register'
    ),
    path('artists/', views.ArtistsList.as_view(), name='artists-list'),
    path('<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),
    path(
        '<int:pk>/update', views.UserUpdateView.as_view(), name='user-update'
    ),
)
