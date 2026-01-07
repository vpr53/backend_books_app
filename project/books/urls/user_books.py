from django.urls import path
from ..views import (
    BooksListAPIView, 
    UsersListAPIView, 
    BooksDetailView, 
)

urlpatterns = [
    path("list/", BooksListAPIView.as_view(), name="books-list"),
    path("detail/<int:id>/", BooksDetailView.as_view(), name="books-detail"), 
    # path(""),
    path("list/users/", UsersListAPIView.as_view(), name="users-list"), 
]
