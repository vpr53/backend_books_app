from rest_framework import serializers
from accounts.models import User
from .models import Book, UserBook


class BooksListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        #exclude = ['google_id', 'pages_count', 'categories']
        fields = ("__all__")


    
class BooksDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("__all__")
        #exclude = ['google_id', 'pages_count', 'categories']

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("__all__")


class UserBookListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBook
        fields = ("__all__")