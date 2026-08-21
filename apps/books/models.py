from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    author_name = models.CharField(max_length=255, db_index=True)
    description = models.TextField()
    content = models.TextField()
    isbn = models.CharField(max_length=13, unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "books"
        ordering = ["title"]
        indexes = [
            models.Index(fields=["title"], name="book_title_idx"),
            models.Index(fields=["author_name"], name="book_author_idx"),
        ]

    def __str__(self):
        return self.title


class Review(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "reviews"
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "book"],
                name="unique_review_per_user_book",
            ),
            models.CheckConstraint(
                condition=models.Q(rating__gte=1) & models.Q(rating__lte=5),
                name="review_rating_range",
            ),
        ]
        indexes = [
            models.Index(fields=["book", "-created_at"], name="review_book_created_idx"),
        ]

    def __str__(self):
        return f"{self.book_id} — {self.user_id} ({self.rating})"
