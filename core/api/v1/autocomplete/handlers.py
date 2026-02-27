from datetime import datetime
from typing import List
import requests
from ninja_jwt.authentication import JWTAuth

from ninja import Router

from .shemas import (
    BooksAutocompleteShemaOut,
    ErrorDetailSchema,
)
from core.project.settings import GOOGLE_BOOKS_API_KEY
from django.conf import settings


api = Router(tags=["Autocomplite"])


@api.get(
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
