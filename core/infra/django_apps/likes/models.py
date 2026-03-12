from django.db import models

from ..accounts.models import UserModels
from ..books.models import UserBookModels


class LikeModel(models.Model):
    user = models.ForeignKey(UserModels, on_delete=models.CASCADE, related_name="likes")

    user_book = models.ForeignKey(
        UserBookModels, on_delete=models.CASCADE, related_name="likes"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "user_book")
        indexes = [
            models.Index(fields=["user", "user_book"]),
        ]

    def __str__(self):
        return f"{self.user} liked {self.user_book}"
