from rest_framework.routers import DefaultRouter
from books.views import UserBookViewSet


router = DefaultRouter()
router.register(r'user/books', UserBookViewSet, basename='user-books')


urlpatterns = router.urls
