from ninja import Router
from books.schema import (
    BookSchemaIn,
    BookSchemaOut,
    BooksAutocompleteShemaOut,
    ErrorSchema,
)
from ninja.errors import HttpError
from books.models import Book
from typing import List
from django.shortcuts import get_object_or_404
import requests
from ninja_jwt.authentication import JWTAuth


api = Router(tags=["Books"])
autocomplite_api = Router(tags=["Autocomplite"])


@api.post(
        "/books/",
        auth=JWTAuth(),
        response={200: BookSchemaOut, 409: ErrorSchema}
    )
def create_book(request, payload: BookSchemaIn):
    if Book.objects.filter(google_id=payload.google_id).exists():
        raise HttpError(409, "Book with this Google ID already exists")
    
    book = Book.objects.create(**payload.dict())
    return book


@api.get(
        "/books/",
        auth=JWTAuth(),
        response=List[BookSchemaOut]
    )
def list_books(request):
    qs = Book.objects.all()
    return qs

@api.get(
        "/books/{book_id}/",
        auth=JWTAuth(),
        response=BookSchemaOut
    )
def get_book(request, book_id:int):
    qs = get_object_or_404(Book, id=book_id)
    return qs


@api.put(
        "/books/{book_id}/",
        auth=JWTAuth(),
        response={200: BookSchemaOut, 409: ErrorSchema}
    )
def update_book(request, book_id: int, payload: BookSchemaIn):
    book = get_object_or_404(Book, id=book_id)

    if (
        payload.google_id != book.google_id
        and Book.objects.filter(google_id=payload.google_id).exclude(id=book_id).exists()
    ):
        return 409, {"detail": "google_id already exists"}
    
    for attr, value in payload.dict().items():
        setattr(book, attr, value)
    book.save()
    return book


@api.delete(
        "/books/{book_id}/",
        auth=JWTAuth(),
    )
def delete_book(request, book_id: int):
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    return 200, {"detail": "The book was successfully deleted"}

@autocomplite_api.get(
    "/autocomplete/",
    response=List[BooksAutocompleteShemaOut],
    )
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
                "categories": ", ".join(volume.get("categories", [])),
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
    

