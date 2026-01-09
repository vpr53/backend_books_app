from django.contrib import admin
from books.models import Book, UserBook

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    name = 'Книги'
    list_display = ["title", "authors", "categories"]


@admin.register(UserBook)
class UserBookAdmin(admin.ModelAdmin):
    name = 'Книги пользователей'
    list_display = ["user", "book", "reading_status"]


