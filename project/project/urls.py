from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI

from books.api import api as books_api
from accounts.api import api as accounts_api

api = NinjaAPI()

api.add_router("/books/", books_api)
api.add_router("/auth/", accounts_api)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", api.urls),
]
