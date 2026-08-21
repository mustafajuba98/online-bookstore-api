import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from apps.books.models import Book, Review

User = get_user_model()


def _user(**overrides):
    data = {"email": "reader@example.com", "password": "strong-pass-123"}
    data.update(overrides)
    return User.objects.create_user(**data)


def _book(**overrides):
    data = {
        "title": "Clean Code",
        "author_name": "Robert C. Martin",
        "description": "A handbook of agile software craftsmanship.",
        "content": "Chapter 1. Clean code is code that is easy to read.",
        "isbn": "9780132350884",
    }
    data.update(overrides)
    return Book.objects.create(**data)


@pytest.mark.django_db
def test_book_str_returns_title():
    book = _book()
    assert str(book) == "Clean Code"


@pytest.mark.django_db
def test_review_is_linked_to_user_and_book():
    user = _user()
    book = _book()
    review = Review.objects.create(user=user, book=book, rating=5, comment="Excellent.")

    assert review.user == user
    assert review.book == book
    assert book.reviews.count() == 1
    assert user.reviews.count() == 1


@pytest.mark.django_db
def test_one_review_per_user_per_book():
    user = _user()
    book = _book()
    Review.objects.create(user=user, book=book, rating=4, comment="Good.")

    with pytest.raises(IntegrityError):
        Review.objects.create(user=user, book=book, rating=5, comment="Again.")


@pytest.mark.django_db
def test_different_users_can_review_the_same_book():
    book = _book()
    first = _user(email="one@example.com")
    second = _user(email="two@example.com")

    Review.objects.create(user=first, book=book, rating=3, comment="Okay.")
    Review.objects.create(user=second, book=book, rating=5, comment="Loved it.")

    assert book.reviews.count() == 2


@pytest.mark.django_db
def test_rating_outside_range_fails_validation():
    user = _user()
    book = _book()
    review = Review(user=user, book=book, rating=6, comment="Invalid.")

    with pytest.raises(ValidationError):
        review.full_clean()
