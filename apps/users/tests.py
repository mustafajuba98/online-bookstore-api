import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_create_user_normalizes_email_and_hashes_password():
    user = User.objects.create_user(email="A@Example.COM", password="strong-pass-123")

    assert user.email == "A@example.com"
    assert user.check_password("strong-pass-123")
    assert user.is_active
    assert not user.is_staff
    assert not user.is_superuser


@pytest.mark.django_db
def test_create_superuser_sets_staff_flags():
    admin = User.objects.create_superuser(
        email="admin@example.com",
        password="strong-pass-123",
    )

    assert admin.is_staff
    assert admin.is_superuser


@pytest.mark.django_db
def test_create_user_requires_email():
    with pytest.raises(ValueError, match="Email is required"):
        User.objects.create_user(email="", password="strong-pass-123")
