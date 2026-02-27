from ninja import Router
from books.schema import (
    BookSchemaIn,
    BookSchemaOut,
    BooksAutocompleteShemaOut,
    ErrorSchema,
    ErrorDetailSchema,
)
from ninja.errors import HttpError
from books.models import BookModels
from typing import List, Optional
from django.shortcuts import get_object_or_404
import requests
from ninja_jwt.authentication import JWTAuth
from project.settings import GOOGLE_BOOKS_API_KEY
from django.conf import settings



api = Router(tags=["Books"])
autocomplite_api = Router(tags=["Autocomplite"])


@autocomplite_api.get(
    "/",
    response={
        200: List[BooksAutocompleteShemaOut],
        502: ErrorDetailSchema,
        400: ErrorDetailSchema,
        500: ErrorDetailSchema,
        },
    auth=JWTAuth(),
    )
def get(request, title: str):
    query = title

    key = getattr(settings, "GOOGLE_BOOKS_API_KEY", None)
    if not key:
        return 400, {
            "error": "Configuration error",
            "details": "Google Books API key is missing"
        }

    url = "https://www.googleapis.com/books/v1/volumes"
    params = {
        "q": f"intitle:{query}",
        "langRestrict": "ru",
        "maxResults": 15,
        "key": GOOGLE_BOOKS_API_KEY
    }

    try:
        r = requests.get(url, params=params, timeout=5)
        r.raise_for_status()
        data = r.json()

        books = []
        for item in data.get("items", []):
            volume = item.get("volumeInfo", {}) or {}
            image_links = volume.get("imageLinks", {}) or {}

            books.append({
                "google_id": item.get("id"),
                "title": volume.get("title", ""),
                "authors": ", ".join(volume.get("authors") or []),
                "publication_year": str(volume.get("publishedDate", ""))[:4],
                "category": ", ".join(volume.get("categories") or []),
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

        return 200, books

    except requests.exceptions.RequestException as e:
        return 502, {
            "error": "External API error",
            "details": str(e)
        }
    
    except Exception as e:
        return 500, {
            "error": "Unexpected error",
            "details": str(e)
        }


@api.post(
        "/",
        auth=JWTAuth(),
        response={200: BookSchemaOut, 409: ErrorSchema}
    )
def create_book(request, payload: BookSchemaIn):
    if BookModels.objects.filter(google_id=payload.google_id).exists():
        return 409, {"detail":"Book with this Google ID already exists"}
    
    book = BookModels.objects.create(**payload.dict())
    return book


@api.get(
        "/",
        auth=JWTAuth(),
        response=List[BookSchemaOut]
    )
def list_books(
    request,        
    authors: Optional[str] = None,
    status: Optional[str] = None, 
    book_id: Optional[int] = None,   
    ):
    qs = BookModels.objects.all()

    if authors:
        qs = qs.filter(authors=authors)

    if status:
        qs = qs.filter(reading_status=status)
    
    if book_id:
        qs = qs.filter(id=book_id)
    
    return qs


@api.put(
        "/",
        auth=JWTAuth(),
        response={200: BookSchemaOut, 409: ErrorSchema}
    )
def update_book(request, book_id: int, payload: BookSchemaIn):
    book = get_object_or_404(BookModels, id=book_id)

    if (
        payload.google_id != book.google_id
        and BookModels.objects.filter(google_id=payload.google_id).exclude(id=book_id).exists()
    ):
        return 409, {"detail": "google_id already exists"}
    
    for attr, value in payload.dict().items():
        setattr(book, attr, value)
    book.save()
    return book


@api.delete("/", auth=JWTAuth())
def delete_book(request, book_id: int):
    book = get_object_or_404(BookModels, id=book_id)
    book.delete()
    return 200, {"detail": "The book was successfully deleted"}



