from rest_framework.routers import DefaultRouter
from books.views import BookAutocompleteAPIView
from django.urls import path


urlpatterns = [
    path('autocomplete/', BookAutocompleteAPIView.as_view(), name='book_autocomplete'),
]
