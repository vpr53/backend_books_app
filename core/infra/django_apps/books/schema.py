from accounts.models import UserModels
from books.models import BookModels, UserBookModels
from ninja import Schema
from ninja.orm import ModelSchema


class BookUserSchemaOut(ModelSchema):
    class Meta:
        model = UserBookModels
        fields = "__all__"


class BookSchemaOut(ModelSchema):
    class Meta:
        model = BookModels
        fields = "__all__"


class BookUserAndBooksSchemaOut(ModelSchema):
    book: BookSchemaOut

    class Meta:
        model = UserBookModels
        exclude = ["book"]


# class BookUserAndBooksSchemaOut(Schema):
#     user_book: int
#     title: str
#     description: str
#     publication_year: int
#     pages_count: int
#     cover_url: Optional[str] = None
#     authors: str
#     categories: Optional[str] = None
#     book_id: int
#     user: int
#     reading_status: str
#     current_page: int
#     rating: int
#     review: str
#     is_public: bool
#     created_at: datetime


class ErrorSchema(Schema):
    detail: str


class ErrorDetailSchema(Schema):
    detail: str
    error: str


class BookUserSchemaIn(ModelSchema):
    class Meta:
        model = UserBookModels
        exclude = ["user", "id", "created_at"]


# class BookUserTestSchemaIn(ModelSchema):
#     class Meta:
#         model = UserBookModels
#         model_fields = ['book_id', 'reading_status', 'current_page', rating] # !!!


class BookUserTestSchemaIn(Schema):
    book_id: int
    reading_status: str
    current_page: int
    rating: int
    review: str
    is_public: bool


class BookSchemaIn(ModelSchema):
    class Meta:
        model = BookModels
        exclude = ["id"]


class BookSchemaOut(ModelSchema):
    class Meta:
        model = BookModels
        fields = "__all__"


class BooksAutocompleteShemaOut(ModelSchema):
    publication_year: str

    class Meta:
        model = BookModels
        exclude = ["id"]


class UserSchemaIn(ModelSchema):
    class Meta:
        model = UserModels
        exclude = ["id", "groups", "user_permissions"]


class UserSchemaOut(ModelSchema):
    class Meta:
        model = UserModels
        fields = "__all__"


class SuccessfulSchema(Schema):
    detail: str
