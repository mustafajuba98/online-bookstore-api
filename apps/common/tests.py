import pytest
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.test import RequestFactory

from apps.common.middleware import JWTAuthenticationMiddleware
from apps.users.tokens import issue_tokens

User = get_user_model()


def _middleware():
    return JWTAuthenticationMiddleware(lambda request: HttpResponse("ok"))


def test_public_register_passes_without_token():
    request = RequestFactory().post("/api/auth/register/")
    response = _middleware()(request)
    assert response.status_code == 200


def test_protected_path_without_token_returns_401():
    request = RequestFactory().get("/api/books/")
    response = _middleware()(request)
    assert response.status_code == 401


def test_protected_path_with_invalid_token_returns_401():
    request = RequestFactory().get(
        "/api/books/",
        HTTP_AUTHORIZATION="Bearer not-a-real-token",
    )
    response = _middleware()(request)
    assert response.status_code == 401


@pytest.mark.django_db
def test_valid_access_token_sets_request_user():
    user = User.objects.create_user(email="reader@example.com", password="strong-pass-123")
    access = issue_tokens(user)["access"]
    request = RequestFactory().get(
        "/api/books/",
        HTTP_AUTHORIZATION=f"Bearer {access}",
    )
    response = _middleware()(request)

    assert response.status_code == 200
    assert request.user == user
