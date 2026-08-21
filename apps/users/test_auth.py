import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from apps.users.tokens import issue_tokens

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_register_returns_tokens(api_client):
    response = api_client.post(
        "/api/auth/register/",
        {
            "email": "new@example.com",
            "password": "strong-pass-123",
            "first_name": "New",
        },
        format="json",
    )

    assert response.status_code == 201
    assert response.data["user"]["email"] == "new@example.com"
    assert response.data["access"]
    assert response.data["refresh"]
    assert User.objects.filter(email="new@example.com").exists()


@pytest.mark.django_db
def test_register_rejects_duplicate_email(api_client):
    User.objects.create_user(email="dup@example.com", password="strong-pass-123")
    response = api_client.post(
        "/api/auth/register/",
        {"email": "dup@example.com", "password": "strong-pass-123"},
        format="json",
    )

    assert response.status_code == 400


@pytest.mark.django_db
def test_login_returns_tokens(api_client):
    User.objects.create_user(email="reader@example.com", password="strong-pass-123")
    response = api_client.post(
        "/api/auth/login/",
        {"email": "reader@example.com", "password": "strong-pass-123"},
        format="json",
    )

    assert response.status_code == 200
    assert response.data["user"]["email"] == "reader@example.com"
    assert response.data["access"]


@pytest.mark.django_db
def test_login_rejects_wrong_password(api_client):
    User.objects.create_user(email="reader@example.com", password="strong-pass-123")
    response = api_client.post(
        "/api/auth/login/",
        {"email": "reader@example.com", "password": "wrong-password"},
        format="json",
    )

    assert response.status_code == 401


@pytest.mark.django_db
def test_refresh_returns_new_access_token(api_client):
    user = User.objects.create_user(email="reader@example.com", password="strong-pass-123")
    refresh = issue_tokens(user)["refresh"]
    response = api_client.post(
        "/api/auth/refresh/",
        {"refresh": refresh},
        format="json",
    )

    assert response.status_code == 200
    assert response.data["access"]
