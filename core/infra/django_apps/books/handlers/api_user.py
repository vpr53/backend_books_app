from ninja import Router
from books.schema import (
    UserSchemaIn,
    UserSchemaOut,
)

from accounts.models import User
from typing import List, Optional
from django.shortcuts import get_object_or_404


api = Router(tags=["Users"])


@api.post("/", response=UserSchemaOut)
def create_user(request, payload: UserSchemaIn):
    user = User.objects.create(**payload.dict())
    return user

@api.get("/", response=List[UserSchemaOut])
def get_users(request, user_id:Optional[int]=None):
    qs = User.objects.all()

    if user_id:
        qs = qs.filter(id=user_id)

    return qs


@api.put("/", response=UserSchemaOut)
def update_user(
        request,
        payload: UserSchemaIn,
        user_id: int
    ):
    user = get_object_or_404(User, id=user_id)
    for attr, value in payload.dict().items():
        setattr(user, attr, value)
    user.save()
    return user


@api.delete("/")
def delete_user(request, user_id: int):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return 200, {"detail": "The user was successfully deleted"}
