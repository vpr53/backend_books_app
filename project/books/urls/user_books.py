from rest_framework.routers import DefaultRouter
from books.views import book_autocomplete
from django.urls import path


urlpatterns = [
    path('autocomplete/', book_autocomplete, name='book_autocomplete'),
]
