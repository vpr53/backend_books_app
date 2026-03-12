from django.test import Client, TestCase

from core.infra.django_apps.accounts.models import UserModels
from core.infra.django_apps.books.models import BookModels, UserBookModels


class BaseBookTestCase(TestCase):
    def setUp(self):
        self.book1 = BookModels.objects.create(
            google_id="674291498137", title="Погода ТОП"
        )
        self.book2 = BookModels.objects.create(
            google_id="674293123123", title="Погода Плохая"
        )
        self.user1 = UserModels.objects.create_user(
            email="user@mail.ru",
            password="12345",
            is_active=True,
        )
        self.user2 = UserModels.objects.create_user(
            email="use2r@mail.ru",
            password="122345",
            is_active=True,
        )

        self.user_book1 = UserBookModels.objects.create(
            book=self.book1, user=self.user1
        )
        self.user_book2 = UserBookModels.objects.create(
            book=self.book2, user=self.user2
        )

        self.client = Client()

    def book_payload(self, **kwargs):
        return {
            "google_id": "test",
            "title": "title",
            "description": "desc",
            "authors": "authors",
            "categories": "1",
            **kwargs,
        }

    def user_book_payload(self, **kwargs):
        return {
            "reading_status": "PLANNED",
            "current_page": "0",
            "rating": "4",
            "review": "GOOD",
            "is_public": True,
            **kwargs,
        }
