import pytest
from django.contrib.auth import get_user_model
from django.core.management import call_command

from apps.books.models import Book, Review

User = get_user_model()


@pytest.mark.django_db
def test_seed_command_is_idempotent():
    call_command("seed_bookstore")
    books = Book.objects.count()
    users = User.objects.count()
    reviews = Review.objects.count()

    assert books >= 30
    assert users >= 10
    assert reviews >= 80

    call_command("seed_bookstore")

    assert Book.objects.count() == books
    assert User.objects.count() == users
    assert Review.objects.count() == reviews
