from ninja import Schema
from ninja.orm import ModelSchema
from books.models import Book, UserBook
from accounts.models import User


class BookUserSchemaOut(ModelSchema):
    class Meta:
        model = UserBook
        fields = "__all__"
        
class ErrorSchema(Schema):
    detail: str

class BookUserSchemaIn(ModelSchema):
    class Meta:
        model = UserBook
        exclude = ["user", "id", "created_at"]

# class BookUserTestSchemaIn(ModelSchema):
#     class Meta:
#         model = UserBook
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
        model = Book
        exclude = ["id"]

class BookSchemaOut(ModelSchema):
    class Meta:
        model = Book
        fields = "__all__"

class BooksAutocompleteShemaOut(ModelSchema):
    publication_year :str

    class Meta:
        model = Book
        exclude = ['id']

class UserSchemaIn(ModelSchema):
    class Meta:
        model = User
        exclude = ["id", "groups", "user_permissions"]


class UserSchemaOut(ModelSchema):
    class Meta:
        model = User
        fields = ("__all__")


class SuccessfulSchema(Schema):
    detail: str
