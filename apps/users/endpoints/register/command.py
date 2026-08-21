from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError

from apps.users.tokens import issue_tokens

User = get_user_model()


class RegisterCommand:
    def execute(self, email, password, first_name="", last_name=""):
        email = User.objects.normalize_email(email)
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError({"email": ["A user with this email already exists."]})
        try:
            validate_password(password)
        except DjangoValidationError as exc:
            raise ValidationError({"password": list(exc.messages)})
        user = User.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        return issue_tokens(user)
