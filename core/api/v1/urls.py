from ninja import Router

from core.api.v1.books.handlers import api as books_api
from core.api.v1.comments.handlers import api as comments_api
from core.api.v1.accounts.handlers import api as accounts_api
from core.api.v1.autocomplete.handlers import api as autocomplete_api
from core.api.v1.user_books.handlers import api as user_books_api

router = Router()

router.add_router("/books/", books_api)
router.add_router("/autocomplete/", autocomplete_api)
router.add_router("/auth/", accounts_api)
router.add_router("/comments/", comments_api)
router.add_router("/user-books/", user_books_api)