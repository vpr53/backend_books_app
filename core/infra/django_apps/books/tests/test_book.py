from core.infra.django_apps.books.models import BookModels
from core.infra.django_apps.utils.decorators import authorized
import json
from .base import BaseBookTestCase


class BookTest(BaseBookTestCase):
    @authorized(user_attr="user1")
    def test_list_books_to_200(self):

        response = self.client.get("/api/books/")

        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 2)
        self.assertEqual({b["id"] for b in data}, {self.book1.id, self.book2.id})
        

    def test_list_book_to_401(self):
        response = self.client.get("/api/books/")

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()["detail"], 'Unauthorized')


    @authorized(user_attr="user1")
    def test_create_book_to_200(self):
        response = self.client.post(
            "/api/books/",
            data=self.book_payload(google_id="qfqiAAAAQBAK", title="Мастер и Маргарита")
        )

        data = response.json()
        self.assertEqual(data["title"], "Мастер и Маргарита")
        self.assertTrue(BookModels.objects.filter(id=data["id"]).exists())
        self.assertEqual(response.status_code, 200)


    def test_create_book_to_401(self):
        response = self.client.post(
            "/api/books/",
            data=json.dumps(self.book_payload(google_id="674291498137", title="Мастер и Маргарита1")),
            content_type="application/json",
        )
        self.assertEqual(response.json()["detail"], 'Unauthorized')
        self.assertEqual(response.status_code, 401)


    @authorized(user_attr="user1")
    def test_create_book_to_409(self):
        response = self.client.post(
            "/api/books/",
            data=self.book_payload(google_id=f"{self.book1.google_id}", title="Мастер и Маргарита1")
            )
        self.assertEqual(response.json()["detail"], 'Book with this Google ID already exists')
        self.assertEqual(response.status_code, 409)

   
    @authorized(user_attr="user1")
    def test_get_book_to_200(self):
        response = self.client.get(f"/api/books/?book_id={self.book1.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]["id"], self.book1.id)



    def test_get_book_to_401(self):
        response = self.client.get(f"/api/books/?book_id={self.book1.id}")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()["detail"], 'Unauthorized')


    @authorized(user_attr="user1")
    def test_update_book_to_200(self):
        book = BookModels.objects.get(google_id=f"{self.book1.google_id}")

        response = self.client.put(
            f"/api/books/?book_id={book.id}",
            data=self.book_payload(google_id=f"{self.book1.google_id}", title="Мастер и Маргарита2")
        )

        book = BookModels.objects.get(google_id=f"{self.book1.google_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["id"], book.id)
        self.assertEqual(response.json()["title"], book.title)
        


    @authorized(user_attr="user1")
    def test_update_book_to_409(self):

        response = self.client.put(
            f"/api/books/?book_id={self.book1.id}",
            data=self.book_payload(google_id=f"{self.book2.google_id}", title="948u2348")
        )

        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.json()["detail"], 'google_id already exists')


    def test_update_book_to_401(self):
        response = self.client.put(
            f"/api/books/?book_id={self.book1.id}",
            data=json.dumps(self.book_payload(google_id=f"{self.book1.google_id}", title="948u2348")),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()["detail"], 'Unauthorized')


    @authorized(user_attr="user1")
    def test_delete_book_to_200(self):

        response = self.client.delete(f"/api/books/?book_id={int(self.book1.id)}")
        book = BookModels.objects.filter(google_id=f"{self.book1.google_id}").first()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["detail"], 'The book was successfully deleted')

        self.assertEqual(book, None)


    def test_delete_book_to_401(self):

        response = self.client.delete(f"/api/books/?book_id={self.book1.id}")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()["detail"], 'Unauthorized')

