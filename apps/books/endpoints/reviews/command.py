from rest_framework.exceptions import NotFound, ValidationError

from apps.books.models import Book, Review


def _book_or_404(book_id):
    book = Book.objects.filter(pk=book_id).only("id").first()
    if book is None:
        raise NotFound("Book not found.")
    return book


class ListReviewsCommand:
    def execute(self, book_id):
        book = _book_or_404(book_id)
        return Review.objects.filter(book=book).select_related("user")


class SubmitReviewCommand:
    def execute(self, user, book_id, rating, comment):
        book = _book_or_404(book_id)
        if Review.objects.filter(user=user, book=book).exists():
            raise ValidationError("Already reviewed.")
        return Review.objects.create(
            user=user,
            book=book,
            rating=rating,
            comment=comment,
        )
