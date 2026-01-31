from django.test import TestCase
from books.models import Book
from django.test import Client
import json

def book_payload(**kwargs):
    return {
        "google_id": "test",
        "title": "title",
        "description": "desc",
        "authors": "authors",
        "categories": "1",
        **kwargs,
    }


class SimpleTest(TestCase):
    def setUp(self):
        self.book1 = Book.objects.create(google_id="674291498137", title="Погода ТОП")
        self.book2 = Book.objects.create(google_id="674293123123", title="Погода Плохая")
        self.client = Client()


    def test_create_book(self):
        response = self.client.post(
            "/api/books/books/",
            data=json.dumps(book_payload(google_id="qfqiAAAAQBAK", title="Мастер и Маргарита")),
            content_type="application/json",
        )
        data = response.json()
        self.assertEqual(data["title"], "Мастер и Маргарита")
        self.assertTrue(Book.objects.filter(id=data["id"]).exists())
        self.assertEqual(response.status_code, 200)

    
    def test_create_book_to_409(self):
        response = self.client.post(
            "/api/books/books/",
            data=json.dumps(book_payload(google_id="674291498137", title="Мастер и Маргарита1")),
            content_type="application/json",
        )
        self.assertEqual(response.json()["detail"], 'Book with this Google ID already exists')
        self.assertEqual(response.status_code, 409)
    


    def test_get_book(self):
        response = self.client.get(f"/api/books/books/{self.book1.id}/")
        # print(response.status_code, response.json())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["id"], self.book1.id)

    def test_get_book_to_404(self):
        response = self.client.get(f"/api/books/books/1000/")
        # print(response.status_code, response.json())
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], 'Not Found')


    def test_list_book(self):
        response = self.client.get("/api/books/books/")
        data = response.json()
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 2)
        self.assertEqual({b["id"] for b in data}, {self.book1.id, self.book2.id})


    def test_update_book(self):

        book = Book.objects.get(google_id="674291498137")

        response = self.client.put(
            f"/api/books/books/{book.id}/",
            data=json.dumps(book_payload(google_id="674291498137", title="Мастер и Маргарита2")),
            content_type="application/json",
        )

        book = Book.objects.get(google_id="674291498137")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["id"], book.id)
        self.assertEqual(response.json()["title"], book.title)


    def test_update_book_to_404_and_409(self):

        response = self.client.put(
            f"/api/books/books/1000/",
            data=json.dumps(book_payload(google_id="674291498137", title="948u2348")),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], 'Not Found')

        response = self.client.put(
            f"/api/books/books/{self.book1.id}/",
            data=json.dumps(book_payload(google_id=f"{self.book2.google_id}", title="948u2348")),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.json()["detail"], 'google_id already exists')


    def test_delete_book(self):

        response = self.client.delete(f"/api/books/books/{self.book1.id}/")

        book = Book.objects.filter(google_id="674291498137").first()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["detail"], 'The book was successfully deleted')

        self.assertEqual(book, None)


    def test_delete_book_to_404(self):

        response = self.client.delete(f"/api/books/books/1000/")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], 'Not Found')

