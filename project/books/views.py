from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404
from rest_framework import viewsets

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

