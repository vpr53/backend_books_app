from typing import List, Optional

from django.shortcuts import get_object_or_404
from ninja import Router
from ninja_jwt.authentication import JWTAuth

from core.infra.django_apps.books.models import UserBookModels
from core.infra.django_apps.comments.models import CommentModels

from .schemas import (
    CommentSchemaIn,
    CommentSchemaOut,
    CommentUpdateSchemaIn,
    ErrorSchema,
)

api = Router(tags=["Comments"])


@api.post(
    "/",
    response={200: CommentSchemaOut, 404: ErrorSchema},
    auth=JWTAuth(),
)
def create_comments(request, payload: CommentSchemaIn, parent: Optional[int] = None):
    user_book = get_object_or_404(UserBookModels, pk=payload.user_book_id)

    parent_comment = None

    if parent:
        parent_comment = get_object_or_404(CommentModels, pk=parent)

        if parent_comment.user_book_id != user_book.id:
            return 404, {"detail": "Parent comment belongs to another book"}

    comment = CommentModels.objects.create(
        user=request.user,
        user_book=user_book,
        parent=parent_comment,
        text=payload.text,
    )

    return comment


@api.get("/", auth=JWTAuth(), response=List[CommentSchemaOut])
def get_comments(
    request,
    me: Optional[bool] = False,
    user_book_id: Optional[int] = None,
    comment_id: Optional[int] = None,
    parent: Optional[int] = None,
):
    qs = CommentModels.objects.all()

    if me:
        qs = qs.filter(user=request.user)

    if comment_id:
        qs = qs.filter(id=comment_id)

    if user_book_id:
        qs = qs.filter(user_book_id=user_book_id)

    if parent:
        qs = qs.filter(parent_id=parent)
    else:
        qs = qs.filter(parent=None)

    return qs


@api.put(
    "/",
    auth=JWTAuth(),
    response={200: CommentSchemaOut, 403: ErrorSchema},
)
def update_comment(
    request,
    payload: CommentUpdateSchemaIn,
    comment_id: int,
):
    user = request.auth
    comment = get_object_or_404(CommentModels, id=comment_id)

    if comment.user == user or user.is_staff():
        comment.text = payload.text
        comment.save()
        return comment
    return 403, {"detail": "Forbidden"}


@api.delete(
    "/",
    auth=JWTAuth(),
)
def delete_comment(request, comment_id: int):
    comment = get_object_or_404(CommentModels, id=comment_id)
    comment.delete()

    return 200, {"detail": "The user was successfully deleted"}
