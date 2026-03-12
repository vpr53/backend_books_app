from ninja import Schema
from ninja.orm import ModelSchema

from core.infra.django_apps.books.models import BookModels


class ErrorDetailSchema(Schema):
    detail: str
    error: str


class BooksAutocompleteShemaOut(ModelSchema):
    publication_year: str

    class Meta:
        model = BookModels
        exclude = ["id"]
