from ninja import Router
from books.schema import (
    BookUserSchemaIn,
    BookUserSchemaOut,
    BookUserTestSchemaIn,
)
from books.models import UserBook
from typing import List
from django.shortcuts import get_object_or_404
from ninja_jwt.authentication import JWTAuth


api = Router(tags=["User_Books"])

@api.post(
        "/users/books/",
        auth=JWTAuth(),
        response=BookUserSchemaOut,
    )
def create_user_book(request, payload: BookUserTestSchemaIn):
    user_book = UserBook.objects.create(
        user=request.user,
        **payload.dict()
    )
    return user_book


@api.get(
        "/users/books/",
        auth=JWTAuth(),
        response=List[BookUserSchemaOut]
    )
def list_users_book(request):
    qs = UserBook.objects.all()
    return qs

@api.get("/users/books/{user_book_id}/", response=BookUserSchemaOut)
def get_user_book(request, user_book_id:int):
    qs = get_object_or_404(UserBook, id=user_book_id)
    return qs


@api.put("/users/books/{user_book_id}/")
def update_user_book(request, user_book_id: int, payload: BookUserSchemaIn):
    user_book = get_object_or_404(UserBook, id=user_book_id)
    for attr, value in payload.dict().items():
        setattr(user_book, attr, value)
    user_book.save()
    return user_book


@api.delete("/users/books/{user_book_id}/")
def delete_user_book(request, user_book_id: int):
    user_book = get_object_or_404(UserBook, id=user_book)
    user_book.delete()
    return 200, {"detail": "The post was successfully deleted"}
