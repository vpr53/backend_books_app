from django.db import models
from accounts.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError


class Book(models.Model):
    google_id = models.CharField("Google ID", max_length=50, unique=True)
    title = models.CharField("Название", max_length=200)
    description = models.TextField("Описание", blank=True)
    publication_year = models.PositiveIntegerField("Год издания", null=True, blank=True)
    pages_count = models.PositiveIntegerField("Количество страниц", null=True, blank=True)
    cover_url = models.URLField("Обложка", null=True, blank=True)
    authors = models.CharField("Авторы", max_length=255, blank=True)
    categories = models.CharField("Жанры", max_length=255, blank=True)

    class Meta:
        verbose_name = "книгу"
        verbose_name_plural = "Книги"

    def __str__(self):
        return self.title
    

class UserBook(models.Model):
    class ReadingStatus(models.TextChoices):
        PLANNED = 'planned', 'Запланировано'
        READING = 'reading', 'Читаю'
        COMPLETED = 'completed', 'Прочитано'
        ABANDONED = 'abandoned', 'Брошено' 
    
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='user_books',
        verbose_name="Пользователь"
    )
    book = models.ForeignKey(
        Book, 
        on_delete=models.CASCADE, 
        related_name='user_books',
        verbose_name="Книга"
    )

    reading_status = models.CharField(
        "Статус чтения",
        max_length=20,
        choices=ReadingStatus.choices,
        default=ReadingStatus.PLANNED,
    )
    current_page = models.PositiveSmallIntegerField(
        "Текущая страница",
        null=True, 
        blank=True
    )
    rating = models.PositiveSmallIntegerField(
        "Оценка",
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    review = models.TextField(
        "Отзыв",
        blank=True
    )
    is_public = models.BooleanField(
        "Публичная",
        default=True
    )
    created_at = models.DateTimeField(
        "Дата добавления",
        auto_now_add=True
    )

    class Meta:
        unique_together = ('user', 'book')
        ordering = ['-created_at']
        verbose_name = "книгу пользователя"
        verbose_name_plural = "Книги пользователей"


'''
    def __str__(self):
        return self.user, self.book
'''
