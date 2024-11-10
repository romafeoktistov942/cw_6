from django.db import models

from mailing.models import NULLABLE


class Blog(models.Model):
    """Класс для модели Попытки"""

    title = models.CharField(
        max_length=50,
        verbose_name="Заголовок",
        help_text="Придумайте заголовок",
        default="Заголовок",
        **NULLABLE,
    )
    post = models.TextField(
        verbose_name="Статья",
        help_text="Введите текс",
        default="Тут должен быть текст новой статьи",
    )
    image = models.ImageField(
        upload_to="blog/", verbose_name="Фото", **NULLABLE, help_text="Загрузите фото"
    )
    views_count = models.PositiveIntegerField(
        default=0, verbose_name="Количество просмотров"
    )
    created_at = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField(
        verbose_name="Дата изменения рассылки", auto_now=True
    )
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано")

    def __str__(self):
        """Строковое представление данных"""
        return f"{self.title}"

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ("title",)
