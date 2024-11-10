from django.db import models
from django.forms import BooleanField, ModelForm
from django import forms
from mailing.models import Mailing, Message, Client


class StyleMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fild_name, fild in self.fields.items():
            if isinstance(fild, BooleanField):
                fild.widget.attrs["class"] = "form-check-input"
            else:
                fild.widget.attrs["class"] = "form-control"


class CustomModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    """Получаем доступ к queryset для фильтрации ManyToMany выводимых данных в форму создания рассылки списка клиентов client_lict"""

    def label_from_instance(self, client_list):
        return "%s" % client_list.email


class MailingForm(StyleMixin, ModelForm):
    def __init__(self, *args, **kwargs):
        """Получаем доступ к queryset для фильтрации ManyToMany выводимых данных в форму создания рассылки списка клиентов client_lict"""
        self.request = kwargs.pop("request")
        super(MailingForm, self).__init__(*args, **kwargs)
        self.fields["client_list"].queryset = Client.objects.filter(
            owner=self.request.user
        )
        self.fields["message_id"].queryset = Message.objects.filter(
            owner=self.request.user
        )

    client_list = CustomModelMultipleChoiceField(queryset=None)

    date_of_first_dispatch = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={"type": "datetime-local", "class": "form-control"}
        ),
        label="Дата первой отправки",
        required=True,
        input_formats=["%Y-%m-%d", "%d-%m-%Y"],
    )

    class Meta:
        model = Mailing
        exclude = ("owner",)


class MailingManagerForm(StyleMixin, ModelForm):
    """Прописываем форму для кастомных прав доступа"""

    def __init__(self, *args, **kwargs):
        """Получаем доступ к queryset для фильтрации ManyToMany выводимых данных в форму создания рассылки списка клиентов client_lict"""
        self.request = kwargs.pop("request")
        super(MailingManagerForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Mailing
        fields = ("is_published",)


class MessageForm(StyleMixin, ModelForm):
    class Meta:
        model = Message
        exclude = (
            "owner",
            "is_published",
        )


class ClientForm(StyleMixin, ModelForm):
    def __init__(self, *args, **kwargs):
        """Получаем доступ к queryset для фильтрации выводимых данных в форму
        Метод для проверки уникальности почт в списке клиентов у пользователя
        """
        self.request = kwargs.pop("request")
        super(ClientForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        """Получаем доступ к queryset для фильтрации выводимых данных в форму
        Метод для проверки уникальности почт в списке клиентов у пользователя
        """
        cleaned_data = self.cleaned_data["email"]
        client_list = Client.objects.filter(owner=self.request.user)
        email_list = [client.email for client in client_list]
        if cleaned_data in email_list:
            raise forms.ValidationError(
                "Клиент с такой почтой уже есть в Вашем списке клиентов"
            )
        return cleaned_data

    class Meta:
        model = Client
        exclude = ("owner",)
