from books.models import UserBook

from utils.decorators import authorized
from .base import BaseBookTestCase


class UserBookTest(BaseBookTestCase):
    @authorized(user_attr="user1")
    def test_list_user_books_to_200(self):

        response = self.client.get("/api/user-books/")

        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 2)
        self.assertEqual({b["id"] for b in data}, {self.user_book1.id, self.user_book2.id})

    
    def test_list_book_to_401(self):
        response = self.client.get("/api/user-books/")

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()["detail"], 'Unauthorized')


    @authorized(user_attr="user1")
    def test_create_user_book_to_200(self):
        response = self.client.post(
            "/api/user-books/",
            data=self.user_book_payload(book_id=self.book2.id)
        )

        data = response.json()

        self.assertEqual(data["book"], self.book2.id)
        self.assertEqual(data["user"], self.user1.id)

        self.assertTrue(UserBook.objects.filter(id=data["book"]).exists())
        self.assertEqual(response.status_code, 200) 


    def test_create_user_book_to_401(self):
        response = self.client.post(
            "/api/user-books/",
            data=self.user_book_payload(book_id=self.book2.id)
        )
        self.assertEqual(response.json()["detail"], 'Unauthorized')
        self.assertEqual(response.status_code, 401)


    """Книга пользователя уже существует"""
    @authorized(user_attr="user1")
    def test_create_user_book_to_409(self):
        response = self.client.post(
            "/api/user-books/",
            data=self.user_book_payload(book_id=self.book1.id)
        )
        self.assertEqual(response.json()["detail"], 'Book with this ID already exists')
        self.assertEqual(response.status_code, 409)


    @authorized(user_attr="user1")
    def test_get_user_book_to_200(self):
        response = self.client.get(
            f"/api/user-books/?user_book_id={self.user_book1.id}/"
        )
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["book"]==self.user_book1.book.id)


    def test_get_user_book_to_401(self):
        response = self.client.get(
            f"/api/user-books/?user_book_id={self.user_book1.id}/"
        )

        data = response.json()

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()["detail"], 'Unauthorized')


    @authorized(user_attr="user1")
    def test_update_user_book_to_200(self):
        response = self.client.put(
            f"/api/user-books/{self.user_book1.id}/",
            data=self.user_book_payload(
                book_id=self.book1.id,
                rating = 5
            )
        )

        data = response.json()
        self.assertEqual(response.status_code, 200)

        ub = UserBook.objects.get(id=self.user_book1.id)
        self.assertEqual(ub.rating, 5)
        self.assertEqual(data["rating"], 5)


    @authorized(user_attr="user1")
    def test_update_user_book_to_404(self):
        response = self.client.put(
            "/api/user-books/1000/",
            data=self.user_book_payload(
                book_id=self.book1.id,
                rating = 5
            )
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], 'Not Found')


    def test_update_user_book_to_401(self):
        response = self.client.put(
            "/api/user-books/1000/",
            data=self.user_book_payload(
                book_id=self.book1.id,
                rating = 5
            )
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()["detail"], 'Unauthorized')


    @authorized(user_attr="user2")
    def test_update_user_book_to_403(self):
        response = self.client.put(
            f"/api/user-books/{self.user_book1.id}/",
            data=self.user_book_payload(
                book_id=self.book1.id,
                rating = 5
            )
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()["detail"], 'Forbidden')


    @authorized(user_attr="user1")
    def test_delete_book_to_200(self):

        response = self.client.delete(f"/api/user-books/{self.user_book1.id}/")

        user_book = UserBook.objects.filter(id=f"{self.user_book1.id}").first()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["detail"], 'The post was successfully deleted')

        self.assertEqual(user_book, None)


    @authorized(user_attr="user1")
    def test_delete_book_to_404(self):

        response = self.client.delete(f"/api/user-books/1000/")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], 'Not Found')


    def test_delete_book_to_401(self):

        response = self.client.delete(f"/api/user-books/{self.user_book1.id}/")

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()["detail"], 'Unauthorized')



    @authorized(user_attr="user2")
    def test_delete_user_book_to_403(self):
        response = self.client.delete(f"/api/user-books/{self.user_book1.id}/")

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()["detail"], 'Forbidden')

    
    # @authorized(user_attr="user1")
    # def test_list_me_user_book_to_200(self):
    #     response = self.client.get("/api/user-books/me/")


    #     print(response.json())
    #     # self.assertEqual(response.status_code, 200)
    #     # self.assertEqual(len(response.json()), 2)
    #     # self.assertEqual(
    #     #     {b["id"] for b in response.json()},
    #     #     {self.user_book1.id, self.user_book2.id}
    #     # )

    # def test_list_me_user_book_401(self):
    #     # Без авторизации
    #     response = self.client.get("/api/user-books/me/")

    #     self.assertEqual(response.status_code, 401)
    #     self.assertEqual(response.json()["detail"], "Unauthorized")