from django.db import models

from core.common.models import BaseModel


class BlogView(BaseModel):
    blog = models.ForeignKey(
        "analytics.Blog",
        on_delete=models.CASCADE,
        related_name="views",
        db_index=True,
    )
    viewer_user = models.ForeignKey(
        "users.User",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="blog_views",
        db_index=True,
    )
    viewer_country = models.ForeignKey(
        "analytics.Country",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="blog_views",
        db_index=True,
    )
    viewed_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = "Blog View"
        verbose_name_plural = "Blog Views"
        ordering = ["-viewed_at"]
        indexes = [
            models.Index(fields=["-viewed_at"]),
            models.Index(fields=["blog", "-viewed_at"]),
            models.Index(fields=["viewer_user", "-viewed_at"]),
            models.Index(fields=["viewer_country", "-viewed_at"]),
            models.Index(fields=["viewer_user", "blog"]),
            models.Index(fields=["viewer_country", "blog"]),
            models.Index(fields=["viewer_user", "viewer_country", "-viewed_at"]),
        ]

    def __str__(self) -> str:
        return f"View of {self.blog.title} at {self.viewed_at}"
