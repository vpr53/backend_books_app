from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from .models import Book
from .serializers import (
    BooksListSerializer,
    BooksDetailSerializer,
    UserListSerializer,
)

from accounts.models import User


class BooksViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['list']:
            return BooksListSerializer
        return BooksDetailSerializer


class UsersListAPIView(APIView):
    # authentication_classes = [JWTAuthentication]  
    # permission_classes = [IsAuthenticated]

    def get(self, request):

        users = User.objects.all()
        serializer = UserListSerializer(instance=users, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK) 
        
