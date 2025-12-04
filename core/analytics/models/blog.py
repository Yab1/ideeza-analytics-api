from django.db import models

from core.common.models import BaseModel


class Blog(BaseModel):
    title = models.CharField(max_length=255, db_index=True)
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="blogs",
        db_index=True,
    )
    country = models.ForeignKey(
        "analytics.Country",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="blogs",
        db_index=True,
    )

    class Meta:
        verbose_name = "Blog"
        verbose_name_plural = "Blogs"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "-created_at"]),
            models.Index(fields=["country", "-created_at"]),
            models.Index(fields=["user", "country", "-created_at"]),
        ]

    def __str__(self) -> str:
        return self.title
