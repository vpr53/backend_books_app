from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import api_view
import requests


from .models import Book, UserBook
from .serializers import (
    BooksListSerializer,
    BooksDetailSerializer,
    UserListSerializer,
    UserBookListSerializer
)

from accounts.models import User
from drf_spectacular.utils import extend_schema_view, extend_schema


@extend_schema_view(
    list=extend_schema(summary="Список книг"),
    retrieve=extend_schema(summary="Детали книги"),
    create=extend_schema(summary="Создание книги"),
    update=extend_schema(summary="Обновление книги"),
    destroy=extend_schema(summary="Удаление книги"),
)
class BooksViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['list']:
            return BooksListSerializer
        return BooksDetailSerializer


@extend_schema_view(
    list=extend_schema(summary="Список пользователей"),
    retrieve=extend_schema(summary="Детали пользователя"),
    create=extend_schema(summary="Создание пользователя"),
    update=extend_schema(summary="Обновление пользователя"),
    destroy=extend_schema(summary="Удаление пользователя"),
)
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['list']:
            return UserListSerializer
        return UserListSerializer


@extend_schema_view(
    list=extend_schema(summary="Список книг пользователя"),
    retrieve=extend_schema(summary="Детали книги пользователя"),
    create=extend_schema(summary="Создание книги пользователя"),
    update=extend_schema(summary="Обновление книги пользователя"),
    destroy=extend_schema(summary="Удаление книги пользователя"),
)
class UserBookViewSet(viewsets.ModelViewSet):
    queryset = UserBook.objects.all()
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['list']:
            return UserBookListSerializer
        return UserBookListSerializer


@api_view(['GET'])
def book_autocomplete(request):
    query = request.GET.get('title', '')
    if not query:
        return Response([])

    url = "https://www.googleapis.com/books/v1/volumes"
    params = {
        "q": f"intitle:{query}",
        "langRestrict": "ru",
        "maxResults": 15
    }

    try:
        r = requests.get(url, params=params)
        data = r.json()
        books = []

        for item in data.get("items", []):
            volume = item.get("volumeInfo", {})
            

            books.append({
                "google_id": item.get("id"),
                "title": volume.get("title"),
                "authors": ", ".join(volume.get("authors", [])),
                "publication_year": volume.get("publishedDate", "")[:4],
                "category": ", ".join(volume.get("categories", [])),
                "description": volume.get("description", ""),
                "cover_url": 
                    volume.get("imageLinks", {}).get("extraLarge") or
                    volume.get("imageLinks", {}).get("large") or
                    volume.get("imageLinks", {}).get("medium") or
                    volume.get("imageLinks", {}).get("small") or
                    volume.get("imageLinks", {}).get("thumbnail") or
                    "",
                "pages_count": volume.get("pageCount"),
            })

        return Response(books)
    except Exception:
        return Response([], status=500)