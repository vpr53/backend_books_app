from books.models import UserBook

from utils.decorators import authorized
from .base import BaseBookTestCase


class UserBookTest(BaseBookTestCase):
    @authorized(user_attr="user1")
    def test_list_user_books_to_200(self):

        response = self.client.get("/api/books/users/books/")

        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 2)
        self.assertEqual({b["id"] for b in data}, {self.user_book1.id, self.user_book2.id})

    
    def test_list_book_to_401(self):
        response = self.client.get("/api/books/users/books/")

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()["detail"], 'Unauthorized')


    @authorized(user_attr="user1")
    def test_create_user_book_to_200(self):
        response = self.client.post(
            "/api/books/users/books/",
            data=self.user_book_payload(book_id=self.book2.id)
        )

        data = response.json()

        self.assertEqual(data["book"], self.book2.id)
        self.assertEqual(data["user"], self.user1.id)

        self.assertTrue(UserBook.objects.filter(id=data["book"]).exists())
        self.assertEqual(response.status_code, 200) 


    def test_create_user_book_to_401(self):
        response = self.client.post(
            "/api/books/users/books/",
            data=self.user_book_payload(book_id=self.book2.id)
        )
        self.assertEqual(response.json()["detail"], 'Unauthorized')
        self.assertEqual(response.status_code, 401)


    """Книга пользователя уже существует"""
    @authorized(user_attr="user1")
    def test_create_user_book_to_409(self):
        response = self.client.post(
            "/api/books/users/books/",
            data=self.user_book_payload(book_id=self.book1.id)
        )
        self.assertEqual(response.json()["detail"], 'Book with this ID already exists')
        self.assertEqual(response.status_code, 409)


    @authorized(user_attr="user1")
    def test_get_user_book_to_200(self):
        response = self.client.get(
            f"/api/books/users/books/{self.user_book1.id}/"
        )

        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["book"]==self.user_book1.book.id)
