import secrets

from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    CreateView,
    UpdateView,
    ListView,
    DetailView,
    DeleteView,
)

from blog.models import Blog
from config.settings import EMAIL_HOST_USER
from users.forms import UserProfileForm, UserRegisterForm, UserManagerForm, UserForm
from users.models import User


class UserListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = User
    permission_required = "users.view_user"


class UserDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = User
    permission_required = "users.view_user"


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token

        user.groups.add(Group.objects.get(name="usersmailing"))
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/users/email-confirm/{token}/"
        send_mail(
            subject="Подтверждение почты",
            message=f"Перейти по ссылке для подтвеждения почты: {url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))


def recovery_password(request):
    if request.method == "POST":
        email = request.POST.get("email")
        token = secrets.token_hex(8)

        user_recovery_password = get_object_or_404(User, email=email)
        user_recovery_password.password = make_password(token)
        user_recovery_password.save()
        send_mail(
            subject="Смена пароля",
            message=f"Автоматически сформированный пароль: {token}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[email],
        )
    return render(request, "users/recovery_password_form.html")


class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm

    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        return self.request.user


def logout_view(request):
    logout(request)
    return redirect("/")


class UserUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = User
    form_class = UserManagerForm
    permission_required = "users.change_user"
    success_url = reverse_lazy(
        "users:user_list",
    )


class UserDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = User
    permission_required = "users:delete_user"
    success_url = reverse_lazy("users:user_list")
