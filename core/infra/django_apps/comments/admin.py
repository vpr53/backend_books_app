from django.contrib import admin
from core.infra.django_apps.comments.models import Comment



@admin.register(Comment)
class BookAdmin(admin.ModelAdmin):
    name = 'Комментарии'
    list_display = ["__str__"]







