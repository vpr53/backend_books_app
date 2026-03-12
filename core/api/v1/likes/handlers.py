from ninja import Router
from ninja_jwt.authentication import JWTAuth

from core.infra.django_apps.books.models import UserBookModels
from core.infra.django_apps.likes.models import LikeModel

from .schemas import ErrorSchema

api = Router(tags=["Likes"])


@api.post(
    "/toggle/",
    response={200: dict, 404: ErrorSchema},
    auth=JWTAuth(),
)
def toggle_like(request, user_book_id: int):
    user_book = UserBookModels.objects.filter(pk=user_book_id).first()

    if not user_book:
        return 404, {"detail": "Invalid user book"}

    like = LikeModel.objects.filter(
        user=request.user, user_book_id=user_book_id
    ).first()

    if like:
        like.delete()
        return {"liked": False}

    LikeModel.objects.create(user=request.user, user_book=user_book)

    return {"liked": True}


@api.get(
    "/count/",
    response={200: dict, 404: ErrorSchema},
)
def count_likes(request, user_book_id: int):
    user_book = UserBookModels.objects.filter(pk=user_book_id).first()

    if not user_book:
        return 404, {"detail": "Invalid user book"}

    count = LikeModel.objects.filter(user_book=user_book).count()

    return {"likes": count}
