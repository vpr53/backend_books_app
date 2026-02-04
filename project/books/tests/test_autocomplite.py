from unittest.mock import patch
from books.handlers.api_book import get
from books.models import Book
from books.tests.base import BaseBookTestCase

class AutocompleteTest(BaseBookTestCase):
    
    @patch("books.handlers.api_book.requests.get")
    def test_autocomplete_success(self, mock_get):
        """Успешный ответ API"""

        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "items": [
                {
                    "id": "1",
                    "volumeInfo": {
                        "title": "Идиот",
                        "authors": ["Фёдор Достоевский"],
                        "publishedDate": "1869",
                        "categories": ["Novel"],
                        "description": "Описание книги",
                        "pageCount": 600,
                        "imageLinks": {"thumbnail": "http://example.com/img.jpg"}
                    }
                }
            ] * 15  
        }

        response_code, data = get(request=None, title="Идиот")

        self.assertEqual(response_code, 200)
        self.assertEqual(len(data), 15)
        self.assertEqual(data[0]["title"], "Идиот")
        self.assertEqual(data[0]["authors"], "Фёдор Достоевский")



    def test_autocomplete_to_400(self):
        """Если API ключ отсутствует → 400"""

        with patch("django.conf.settings.GOOGLE_BOOKS_API_KEY", None):
            response_code, data = get(request=None, title="Идиот")
            self.assertEqual(response_code, 400)

            
    def test_autocomplete_to_401(self):
        """Если пользователь не авторизован → 401"""

        response = self.client.get("/api/books/autocomplete/?title=Идиот")
        self.assertEqual(response.status_code, 401)




