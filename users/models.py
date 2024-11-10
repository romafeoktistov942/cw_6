from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {"null": True, "blank": True}


class User(AbstractUser):
    """Класс для модели пользователей"""

    username = None
    email = models.EmailField(
        unique=True, verbose_name="Почта", help_text="Укажите почту"
    )

    avatar = models.ImageField(
        upload_to="users/avatars/",
        verbose_name="Фото",
        **NULLABLE,
        help_text="Загрузите фото",
    )
    phone = models.CharField(
        max_length=35,
        verbose_name="Телефон",
        help_text="Введите номер телефона",
        **NULLABLE,
    )
    country = models.CharField(
        max_length=50, verbose_name="Страна", help_text="Введите страну", **NULLABLE
    )

    token = models.CharField(max_length=100, verbose_name="Токен", **NULLABLE)

    is_active = models.BooleanField(
        default=True, verbose_name="Активация", help_text="Активируйте пользователя"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        """Строковое представление данных"""
        return f"{self.email}"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

        permissions = [
            ("Can_edit_is_active", "Can edit is active"),
        ]
