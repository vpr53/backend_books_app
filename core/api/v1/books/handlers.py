from ninja import Router
from .chemas import (
    BookSchemaIn,
    BookSchemaOut,
    ErrorSchema,
)
from core.infra.django_apps.books.models import BookModels
from typing import List, Optional
from django.shortcuts import get_object_or_404
from ninja_jwt.authentication import JWTAuth




api = Router(tags=["Books"])


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



