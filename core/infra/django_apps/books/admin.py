from django.contrib import admin
from core.infra.django_apps.books.models import BookModels, UserBookModels


@admin.register(BookModels)
class BookAdmin(admin.ModelAdmin):
    name = 'Книги'
    list_display = ["title", "authors", "categories"]


@admin.register(UserBookModels)
class UserBookAdmin(admin.ModelAdmin):
    name = 'Книги пользователей'
    list_display = ["user", "book", "reading_status"]


