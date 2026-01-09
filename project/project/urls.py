
from django.contrib import admin
from django.urls import include, path

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path('admin/', admin.site.urls),
    path("api/auth/", include("accounts.urls")),
    path("api/books/", include("books.urls.books")),
    path("api/books/", include("books.urls.user_books")),
]