from ninja import Schema
from ninja.orm import ModelSchema
from comments.models import Comment


class CommentSchemaOut(ModelSchema):
    class Meta:
        model = Comment
        fields = "__all__"


class CommentSchemaIn(Schema):
    user_book_id: int
    text: str
    

class CommentUpdateSchemaIn(Schema):
    text: str 

class ErrorSchema(Schema):
    detail: str

class UserSchema(Schema):
    email: str
