from django.contrib.auth.views import LoginView
from django.urls import path
from django.views.decorators.cache import cache_page

from users.apps import UsersConfig
from users.views import (
    logout_view,
    RegisterView,
    ProfileView,
    email_verification,
    recovery_password,
    UserListView,
    UserDetailView,
    UserUpdateView,
    UserDeleteView,
)

app_name = UsersConfig.name

urlpatterns = [
    path("", LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", logout_view, name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("email-confirm/<str:token>/", email_verification, name="email-confirm"),
    path("recovery/", recovery_password, name="recovery"),
    path("users/", cache_page(60)(UserListView.as_view()), name="user_list"),
    path("users/<int:pk>/view", UserDetailView.as_view(), name="user_detail"),
    path("users/<int:pk>/update/", UserUpdateView.as_view(), name="user_update"),
    path("users/<int:pk>/delete/", UserDeleteView.as_view(), name="user_delete"),
]
