from rest_framework.routers import DefaultRouter

from books.views import (
    BooksViewSet, 
    UserViewSet, 
    UserBookViewSet,
    )


router = DefaultRouter()
router.register(r'books', BooksViewSet, basename='books')
router.register(r'users', UserViewSet, basename='users')
router.register(r'user/books', UserBookViewSet, basename='user-books')



urlpatterns = router.urls 

