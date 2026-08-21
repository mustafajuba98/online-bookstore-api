from django.db.models import Count
from rest_framework.exceptions import NotFound

from apps.books.models import Book


class GetBookCommand:
    def execute(self, book_id):
        book = (
            Book.objects.annotate(reviews_count=Count("reviews"))
            .filter(pk=book_id)
            .first()
        )
        if book is None:
            raise NotFound("Book not found.")
        return book
