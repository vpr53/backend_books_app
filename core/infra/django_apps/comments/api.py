from typing import List, Optional
from ninja import Router
from ninja_jwt.authentication import JWTAuth

from comments.schema import (
    CommentSchemaIn,
    CommentSchemaOut,
    ErrorSchema,
    UserSchema,
    CommentUpdateSchemaIn,
    )
from comments.models import Comment
from books.models import UserBook

from django.shortcuts import get_object_or_404

api = Router(tags=["Comments"])

@api.post(
        "/",
        response={200: CommentSchemaOut, 404: ErrorSchema},
        auth=JWTAuth(),
    )
def create_comments(request, payload: CommentSchemaIn):

    user_book = UserBook.objects.filter(
        pk=payload.user_book_id
    ).first()

    if not user_book:
        return 404, {"detail": "Invalid user book"}

    comment = Comment.objects.create(
        user=request.user,
        user_book=user_book,
        text=payload.text
    )
    return comment



@api.get(
        "/",
        auth=JWTAuth(),
        response=List[CommentSchemaOut]
    )
def get_comments(
    request,
    me: Optional[bool] = True,        
    user_book_id: Optional[int] = None, 
    comment_id: Optional[int] = None,   
    ):
    qs = Comment.objects.all()

    if me:
        qs = qs.filter(user=request.user)
    
    if comment_id:
        qs = qs.filter(id=comment_id)
    
    if user_book_id:
        qs = qs.filter(user_book=user_book_id)
    return qs


@api.put(
        "/",
        # "/{comment_id}/",
        auth=JWTAuth(),
        response={200: CommentSchemaOut, 403: ErrorSchema},
    )
def update_comment(
        request,
        payload: CommentUpdateSchemaIn,        
        comment_id: int,
    ):
    user = request.auth
    comment = get_object_or_404(Comment, id=comment_id)

    if comment.user == user or user.is_staff():
        comment.text = payload.text
        comment.save()
        return comment
    return 403, {"detail": "Forbidden"}

                    
@api.delete('/',auth=JWTAuth(),)
def delete_comment(
        request,
        comment_id: int
    ):
    
    comment = get_object_or_404(Comment, id=comment_id)
    comment.delete()

    return 200, {"detail": "The user was successfully deleted"}
