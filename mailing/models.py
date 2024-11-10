from django.db import models

from users.models import User

NULLABLE = {"null": True, "blank": True}


class Message(models.Model):
    """Класс для модели Сообщения"""

    title = models.CharField(
        max_length=100,
        default="Рассылка",
        verbose_name="Заголовок",
        help_text="Введите заголовок",
    )
    message = models.TextField(verbose_name="Сообщение", help_text="Введите текс")
    image = models.ImageField(
        upload_to="blog/", verbose_name="Фото", **NULLABLE, help_text="Загрузите фото"
    )
    created_at = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    update_at = models.DateTimeField(verbose_name="Дата изменения", auto_now=True)
    owner = models.ForeignKey(
        User,
        **NULLABLE,
        verbose_name="Владелец",
        help_text="Введите владельца",
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        """Строковое представление данных"""
        return f"{self.title}"

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ("title",)


class Client(models.Model):
    """Класс для модели Клиент"""

    email = models.CharField(
        max_length=100,
        verbose_name="Почта для рассылки",
        help_text="Заполните почту для рассылки",
    )
    name = models.CharField(
        max_length=100, verbose_name="ФИО", help_text="Введите имя клиента", **NULLABLE
    )
    comment = models.TextField(
        verbose_name="Комментарий", help_text="Добавьте комментарий", **NULLABLE
    )
    owner = models.ForeignKey(
        User,
        **NULLABLE,
        verbose_name="Владелец",
        help_text="Введите владельца",
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        """Строковое представление данных"""
        return f"{self.name} {self.email}"

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
        ordering = ("name",)


class Mailing(models.Model):
    """Класс для модели Рассылки"""

    date_of_first_dispatch = models.DateTimeField(
        verbose_name="Дата первой отправки", **NULLABLE
    )
    periodicity = models.CharField(
        max_length=1,
        choices={"D": "Раз в день", "W": "Раз в неделю", "M": "Раз в месяц"},
        verbose_name="Периодичность отправки",
        help_text="Выберите периодичность отправки",
        **NULLABLE,
    )
    status = models.CharField(
        max_length=20,
        choices={"C": "Создана", "W": "Запущена", "F": "Завершена"},
        verbose_name="Статус рассылки",
    )
    created_at = models.DateTimeField(
        verbose_name="Дата создания рассылки", auto_now_add=True
    )
    update_at = models.DateTimeField(
        verbose_name="Дата изменения рассылки", auto_now=True
    )
    message_id = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        verbose_name="Сообщение",
        help_text="Выберите сообщение",
        related_name="Mailing",
    )
    client_list = models.ManyToManyField(
        Client,
        verbose_name="Клиенты",
        help_text="Выберите клиентов для рассылки",
        related_name="client",
    )
    owner = models.ForeignKey(
        User,
        **NULLABLE,
        verbose_name="Владелец",
        help_text="Введите владельца",
        on_delete=models.SET_NULL,
    )
    is_published = models.BooleanField(
        default=True, verbose_name="Опубликовано", help_text="Отметьте для активации"
    )

    def __str__(self):
        """Строковое представление данных"""
        return f"{self.message_id.title}"

    def get_clients(self):
        """Метод для вывода списка ManyToManyField client_list в admin панели"""
        return ", ".join([client.email for client in self.client_list.all()])

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        ordering = ("status",)
        permissions = [
            ("Can_is_published", "Can is published"),
        ]


class Attempt(models.Model):
    """Класс для модели Попытки"""

    date_last_attempt = models.DateTimeField(verbose_name="Дата попытки", auto_now=True)
    status = models.BooleanField(verbose_name="Статус рассылки")
    server_response = models.CharField(max_length=50, verbose_name="Ответ сервера")
    mailing_id = models.ForeignKey(
        Mailing,
        on_delete=models.CASCADE,
        verbose_name="Рассылка",
        help_text="Выберите рассылку",
        related_name="Attempt",
    )
    owner = models.ForeignKey(
        User,
        **NULLABLE,
        verbose_name="Владелец",
        help_text="Введите владельца",
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        """Строковое представление данных"""
        return f"{self.date_last_attempt}"

    class Meta:
        verbose_name = "Попытка"
        verbose_name_plural = "Попытки"
        ordering = ("status",)
