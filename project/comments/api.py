from typing import List
from ninja import Router
from ninja_jwt.authentication import JWTAuth

from comments.schema import (
    CommentSchemaIn,
    CommentSchemaOut,
    ErrorSchema,
    UserSchema,
    )
from comments.models import Comment
from books.models import UserBook

from django.shortcuts import get_object_or_404

api = Router(tags=["Comments"])

@api.post(
        "/comments/",
        response={200: CommentSchemaOut, 404: ErrorSchema},
        auth=JWTAuth(),
    )
def create_comments(request, payload: CommentSchemaIn):

    user_book = UserBook.objects.filter(
        pk=payload.user_book_id
    )

    if not user_book:
        return 404, {"detail": "Invalid user book"}

    comment = Comment.objects.create(
        user=request.auth,
        user_book=user_book,
        text=payload.text
    )
    return comment



@api.get("/comments/", response=List[CommentSchemaOut])
def list_all_comments(request):
    return Comment.objects.all()


@api.get("/comments/user-book/{user_book_id}/", response=List[CommentSchemaOut])
def list_user_book_comments(request, user_book_id: int):
    user_book = get_object_or_404(UserBook, pk=user_book_id)
    
    return user_book.comments.all()


        
@api.get("/comments/{comment_id}/", response=CommentSchemaOut)
def get_comment(request, comment_id: int):
    comment = get_object_or_404(Comment, pk=comment_id)
    return comment

# @api.put("/books/{book_id}/")
# def update_book(request, book_id: int, payload: BookSchemaIn):
#     book = get_object_or_404(Book, id=book_id)
#     for attr, value in payload.dict().items():
#         setattr(book, attr, value)
#     book.save()
#     return book


# @api.delete("/books/{book_id}/")
# def delete_book(request, book_id: int):
#     book = get_object_or_404(Book, id=book_id)
#     book.delete()
#     return 204, None
