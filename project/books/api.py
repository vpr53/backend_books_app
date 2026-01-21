from ninja import Router
from books.schema import (
    BookSchemaIn,
    BookUserSchemaIn,
    BookUserSchemaOut,
    BookSchemaOut,
    BooksAutocompleteShemaOut,
    UserSchemaIn,
    UserSchemaOut,
)
from ninja.errors import HttpError
from books.models import Book, UserBook
from accounts.models import User
from typing import List
from django.shortcuts import get_object_or_404
import requests

api = Router(tags=["Books"])


@api.post("/books/")
def create_book(request, payload: BookSchemaIn):
    book = Book.objects.create(**payload.dict())
    return book

@api.get("/books/", response=List[BookSchemaOut])
def list_books(request):
    qs = Book.objects.all()
    return qs

@api.get("/books/{book_id}/", response=BookSchemaOut)
def get_book(request, book_id:int):
    qs = get_object_or_404(Book, id=book_id)
    return qs


@api.put("/books/{book_id}/")
def update_book(request, book_id: int, payload: BookSchemaIn):
    book = get_object_or_404(Book, id=book_id)
    for attr, value in payload.dict().items():
        setattr(book, attr, value)
    book.save()
    return book


@api.delete("/books/{book_id}/")
def delete_book(request, book_id: int):
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    return 204, None

@api.get("/autocomplete/", response=List[BooksAutocompleteShemaOut])
def get(request, title: str):
    query = title

    url = "https://www.googleapis.com/books/v1/volumes"
    params = {
        "q": f"intitle:{query}",
        "langRestrict": "ru",
        "maxResults": 15
    }

    try:
        r = requests.get(url, params=params, timeout=5)
        r.raise_for_status()
        data = r.json()

        books = []
        for item in data.get("items", []):
            volume = item.get("volumeInfo", {})
            image_links = volume.get("imageLinks", {})

            books.append({
                "google_id": item.get("id"),
                "title": volume.get("title"),
                "authors": ", ".join(volume.get("authors", [])),
                "publication_year": volume.get("publishedDate", "")[:4],
                "category": ", ".join(volume.get("categories", [])),
                "description": volume.get("description", ""),
                "cover_url": (
                    image_links.get("extraLarge") or
                    image_links.get("large") or
                    image_links.get("medium") or
                    image_links.get("small") or
                    image_links.get("thumbnail") or
                    ""
                ),
                "pages_count": volume.get("pageCount"),
            })

        return books

    except requests.exceptions.RequestException as e:
        raise HttpError(502, str(e))
    except Exception as e:
        return {"error": "Unexpected error", "details": str(e)}
    

@api.post("/users/")
def create_user(request, payload: UserSchemaIn):
    user = User.objects.create(**payload.dict())
    return user

@api.get("/users/", response=List[UserSchemaOut])
def list_users(request):
    qs = User.objects.all()
    return qs

@api.get("/users/{user_id}/", response=BookSchemaOut)
def get_user(request, user_id:int):
    qs = get_object_or_404(User, id=user_id)
    return qs


@api.put("/users/{user_id}/")
def update_user(request, user_id: int, payload: UserSchemaIn):
    user = get_object_or_404(User, id=user_id)
    for attr, value in payload.dict().items():
        setattr(user, attr, value)
    user.save()
    return user


@api.delete("/users/{user_id}/")
def delete_user(request, user_id: int):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return 204, None


@api.post("/users/books/")
def create_user_book(request, payload: BookUserSchemaIn):
    user_book = UserBook.objects.create(**payload.dict())
    return user_book

@api.get("/users/books/", response=List[BookUserSchemaOut])
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
    return 204, None