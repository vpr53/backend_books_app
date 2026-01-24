from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI

from books.api import api as books_api
from books.api import autocomplite_api 

from accounts.api import api as accounts_api

from ninja_jwt.controller import (     
    TokenObtainPairController,
)

from ninja_extra import NinjaExtraAPI, api_controller

@api_controller("/auth/token", tags=["Auth"])
class CustomJWTController(
    TokenObtainPairController,
):
    pass

api = NinjaExtraAPI()
api.register_controllers(CustomJWTController)


api.add_router("/books/", books_api)
api.add_router("/books/", autocomplite_api)
api.add_router("/auth/", accounts_api)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
]
