import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from apps.books.models import Book
from apps.users.tokens import issue_tokens

User = get_user_model()


@pytest.fixture
def auth_client(db):
    user = User.objects.create_user(email="reader@example.com", password="strong-pass-123")
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {issue_tokens(user)['access']}")
    return client


def _book(**overrides):
    data = {
        "title": "Clean Code",
        "author_name": "Robert C. Martin",
        "description": "A handbook of agile software craftsmanship.",
        "content": "Full book text that should not appear in the list.",
        "isbn": "9780132350884",
    }
    data.update(overrides)
    return Book.objects.create(**data)


@pytest.mark.django_db
def test_list_books_requires_auth():
    response = APIClient().get("/api/books/")
    assert response.status_code == 401


@pytest.mark.django_db
def test_list_books_omits_content_and_includes_reviews_count(auth_client):
    _book()
    response = auth_client.get("/api/books/")

    assert response.status_code == 200
    assert response.data["count"] == 1
    book = response.data["results"][0]
    assert book["title"] == "Clean Code"
    assert book["reviews_count"] == 0
    assert "content" not in book


@pytest.mark.django_db
def test_list_books_is_paginated(auth_client):
    for index in range(21):
        _book(title=f"Book {index:02d}", isbn=None, content="x")

    response = auth_client.get("/api/books/")

    assert response.status_code == 200
    assert response.data["count"] == 21
    assert len(response.data["results"]) == 20
    assert response.data["next"] is not None


@pytest.mark.django_db
def test_list_books_search_filters_by_title(auth_client):
    _book(title="Clean Code", isbn="1111111111111")
    _book(title="The Pragmatic Programmer", isbn="2222222222222", content="other")

    response = auth_client.get("/api/books/", {"search": "pragmatic"})

    assert response.status_code == 200
    assert response.data["count"] == 1
    assert response.data["results"][0]["title"] == "The Pragmatic Programmer"


@pytest.mark.django_db
def test_book_detail_returns_content(auth_client):
    book = _book()
    response = auth_client.get(f"/api/books/{book.id}/")

    assert response.status_code == 200
    assert response.data["content"].startswith("Full book text")
    assert response.data["reviews_count"] == 0


@pytest.mark.django_db
def test_book_detail_not_found(auth_client):
    response = auth_client.get("/api/books/999/")
    assert response.status_code == 404
