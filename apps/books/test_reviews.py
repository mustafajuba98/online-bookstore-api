import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from apps.books.models import Book, Review
from apps.users.tokens import issue_tokens

User = get_user_model()


@pytest.fixture
def reader(db):
    return User.objects.create_user(email="reader@example.com", password="strong-pass-123")


@pytest.fixture
def auth_client(reader):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {issue_tokens(reader)['access']}")
    return client


@pytest.fixture
def book(db):
    return Book.objects.create(
        title="Clean Code",
        author_name="Robert C. Martin",
        description="A handbook of agile software craftsmanship.",
        content="Full book text that should not appear in the list.",
        isbn="9780132350884",
    )


@pytest.mark.django_db
def test_list_reviews_requires_auth(book):
    response = APIClient().get(f"/api/books/{book.id}/reviews/")
    assert response.status_code == 401


@pytest.mark.django_db
def test_submit_review(auth_client, book):
    response = auth_client.post(
        f"/api/books/{book.id}/reviews/",
        {"rating": 5, "comment": "Excellent."},
        format="json",
    )

    assert response.status_code == 201
    assert response.data["rating"] == 5
    assert response.data["comment"] == "Excellent."
    assert Review.objects.filter(book=book).count() == 1


@pytest.mark.django_db
def test_submit_review_rejects_duplicate(auth_client, reader, book):
    Review.objects.create(user=reader, book=book, rating=2, comment="Not yet.")
    response = auth_client.post(
        f"/api/books/{book.id}/reviews/",
        {"rating": 4, "comment": "Better on a second read."},
        format="json",
    )

    assert response.status_code == 400
    assert "Already reviewed" in str(response.data)
    assert Review.objects.filter(book=book, user=reader).count() == 1
    assert Review.objects.get(book=book, user=reader).comment == "Not yet."


@pytest.mark.django_db
def test_list_reviews_includes_other_users(auth_client, book):
    other = User.objects.create_user(email="other@example.com", password="strong-pass-123")
    Review.objects.create(user=other, book=book, rating=5, comment="Loved it.")

    response = auth_client.get(f"/api/books/{book.id}/reviews/")

    assert response.status_code == 200
    assert response.data["count"] == 1
    assert response.data["results"][0]["comment"] == "Loved it."
    assert response.data["results"][0]["user"]["email"] == "other@example.com"


@pytest.mark.django_db
def test_review_rejects_invalid_rating(auth_client, book):
    response = auth_client.post(
        f"/api/books/{book.id}/reviews/",
        {"rating": 9, "comment": "Impossible."},
        format="json",
    )
    assert response.status_code == 400


@pytest.mark.django_db
def test_reviews_for_missing_book(auth_client):
    response = auth_client.get("/api/books/999/reviews/")
    assert response.status_code == 404
