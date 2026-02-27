from ninja import Router
from books.schema import (
    BookUserSchemaIn,
    BookUserSchemaOut,
    BookUserTestSchemaIn,
    ErrorSchema,
    SuccessfulSchema,
    BookUserAndBooksSchemaOut,
)
from books.models import UserBook
from typing import List, Optional
from django.shortcuts import get_object_or_404
from ninja_jwt.authentication import JWTAuth


api = Router(tags=["User_Books"])



@api.get(
        "/full/",
        auth=JWTAuth(),
        response={
        200: List[BookUserAndBooksSchemaOut],
        401: ErrorSchema,
        }
    )
def list_user_books_full(
        request,
        me: Optional[bool] = False,
        authors: Optional[str] = None,
        status: Optional[str] = None, 
        user_book_id: Optional[int] = None,   
        title: Optional[str] = None
    ):
    """
    List UserBooks.
    - ?me=true → только текущий пользователь
    - без параметра → все записи
    """
    qs = UserBook.objects.select_related("book").all()

    if me:
        qs = qs.filter(user=request.user)

    if authors:
        qs = qs.filter(authors=authors)

    if status:
        qs = qs.filter(reading_status=status)
    
    if user_book_id:
        qs = qs.filter(id=user_book_id)
    
    if title:
        qs = qs.filter(title=title)

    return qs


@api.post(
        "/",
        auth=JWTAuth(),
        response={200: BookUserSchemaOut, 409: ErrorSchema},
    )
def create_user_book(request, payload: BookUserTestSchemaIn):
    if UserBook.objects.filter(
        book_id=payload.book_id,
        user=request.user
    ).exists():
        return 409, {"detail": "BookModels with this ID already exists"}
    user_book = UserBook.objects.create(
        user=request.user,
        **payload.dict()
    )   


    return user_book


@api.get(
        "/",
        auth=JWTAuth(),
        response=List[BookUserSchemaOut]
    )
def list_users_book(
    request,        
    me: Optional[bool] = True,
    authors: Optional[str] = None,
    status: Optional[str] = None, 
    user_book_id: Optional[int] = None,   
    title: Optional[str] = None,
    ):
    qs = UserBook.objects.all()

    if me:
        qs = qs.filter(user=request.user)

    if authors:
        qs = qs.filter(authors=authors)

    if status:
        qs = qs.filter(reading_status=status)
    
    if user_book_id:
        qs = qs.filter(id=user_book_id)
    
    if title:
        qs = qs.filter(title=title)


    return qs



@api.put(
        "/{user_book_id}/",
        auth=JWTAuth(),
        response={
            200: BookUserSchemaOut,
            404: ErrorSchema,
            403: ErrorSchema,
        }
    )
def update_user_book(request, user_book_id: int, payload: BookUserTestSchemaIn):
    user_book = UserBook.objects.filter(id=user_book_id).first()
    if not user_book:
        return 404, {"detail": "Not Found"}

    if user_book.user != request.user and not request.user.is_superuser:
        return 403, {"detail": "Forbidden"}

    for attr, value in payload.dict().items():
        setattr(user_book, attr, value)
    user_book.save()
    return user_book


@api.delete(
        "/{user_book_id}/",
        auth=JWTAuth(),
        response={
            200: SuccessfulSchema,
            404: ErrorSchema,
            403: ErrorSchema,
        }
    )
def delete_user_book(request, user_book_id: int):
    user_book = get_object_or_404(UserBook, id=user_book_id)

    if user_book.user != request.user and not request.user.is_superuser:
        return 403, {"detail": "Forbidden"}
    
    user_book.delete()
    return 200, {"detail": "The post was successfully deleted"}


# @api.get(
#     "/me/",
#     auth=JWTAuth(),
#     response={200: List[BookUserAndBooksSchemaOut], 401: ErrorSchema},
# )
# def get_user_user_book(request):
#     user_books = request.user.user_books.all()
#     result = []

#     for item in user_books:
#         book = item.book  
#         result.append(BookUserAndBooksSchemaOut(
#             user_book=item.id,
#             book_id=book.id,
#             user=item.user.id,
#             title=book.title,
#             description=book.description,
#             publication_year=book.publication_year,
#             pages_count=book.pages_count,
#             cover_url=book.cover_url,
#             authors=book.authors,
#             categories=book.categories,
#             reading_status=item.reading_status,
#             current_page=item.current_page,
#             rating=item.rating,
#             review=item.review,
#             is_public=item.is_public,
#             created_at=item.created_at
#         ))

#     return result


# @api.get(
#     "/me/",
#     auth=JWTAuth(),
#     # response={
#     #     # 200: List[BookUserAndBooksSchemaOut],
#     #     200: List[BookUserSchemaOut],
#     #     401: ErrorSchema
#     # },
# )
# def get_user_user_book(request):
#     return request.user.id
#     # return ("ok"
#     #     request.user.user_books.all()
#     #     # .select_related("book")

#     # )

#     # return "OK"



