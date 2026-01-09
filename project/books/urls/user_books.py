from rest_framework.routers import DefaultRouter
from books.views import BookAutocompleteAPIView
from django.urls import path


urlpatterns = [
    path('autocomplete/<str:title>/', BookAutocompleteAPIView.as_view(), name='book_autocomplete'),
]
