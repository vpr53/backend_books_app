from django.contrib import admin
from django.urls import path

from books.handlers.api_user import api as users_api
from books.handlers.api_user_book import api as user_books_api
from books.handlers.api_book import api as books_api
from books.handlers.api_book import autocomplite_api

from comments.api import api as comments_api
from accounts.api import api as accounts_api

from ninja_jwt.controller import (     
    NinjaJWTDefaultController,
)
from ninja import Swagger
from ninja_extra import NinjaExtraAPI
from ninja import Redoc

    
api = NinjaExtraAPI(title="Book API")

api.register_controllers(NinjaJWTDefaultController)


api.add_router("/books/", books_api)
api.add_router("/autocomplete/", autocomplite_api)
api.add_router("/auth/", accounts_api)
api.add_router("/comments/", comments_api)
api.add_router("/users/", users_api)
api.add_router("/user-books/", user_books_api)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
]
