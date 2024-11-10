from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm

from mailing.forms import StyleMixin
from users.models import User


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "password1", "password2")


class UserForm(StyleMixin, ModelForm):
    class Meta:
        model = User
        fields = "__all__"


class UserManagerForm(ModelForm):
    """Прописываем форму для кастомных прав доступа"""

    class Meta:
        model = User
        fields = ("is_active",)


class UserProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "phone", "avatar")

    def __init__(self, *args, **kwargs):
        """Что бы скрыть в форме "Пароль не задан" """
        super().__init__(*args, **kwargs)

        self.fields["password"].widget = forms.HiddenInput()
