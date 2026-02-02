from ninja import Router
from books.schema import (
    UserSchemaIn,
    UserSchemaOut,
)

from accounts.models import User
from typing import List
from django.shortcuts import get_object_or_404


api = Router(tags=["Users"])


@api.post("/users/", response=UserSchemaOut)
def create_user(request, payload: UserSchemaIn):
    user = User.objects.create(**payload.dict())
    return user

@api.get("/users/", response=List[UserSchemaOut])
def list_users(request):
    qs = User.objects.all()
    return qs

@api.get("/users/{user_id}/", response=UserSchemaOut)
def get_user(request, user_id:int):
    qs = get_object_or_404(User, id=user_id)
    return qs


@api.put("/users/{user_id}/", response=UserSchemaOut)
def update_user(request, user_id: int, payload: UserSchemaIn):
    user = get_object_or_404(User, id=user_id)
    for attr, value in payload.dict().items():
        setattr(user, attr, value)
    user.save()
    return user


@api.delete("/users/{user_id}/")
def delete_user(request, user_id: int):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return 200, {"detail": "The user was successfully deleted"}
