from rest_framework import serializers
from accounts.models import User
from .models import Book


class BooksListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        exclude = ['google_id', 'pages_count', 'categories']

    
class BooksDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("__all__")


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("__all__")