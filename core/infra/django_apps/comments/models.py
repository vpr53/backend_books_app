from django.db import models
from core.infra.django_apps.accounts.models import UserModels
from core.infra.django_apps.books.models import UserBookModels


class CommentModels(models.Model):
    user_book = models.ForeignKey(
        UserBookModels,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Книга пользователя"
    )
    user = models.ForeignKey(
        UserModels,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Автор"
    )
    text = models.TextField("Текст")

    created_at = models.DateTimeField(
        "Опубликован",
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        "Обновлён",
        auto_now=True
    )

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=["user_book", "created_at"]),
        ]

    def __str__(self):
        return f"{self.user}: {self.text[:30]}"