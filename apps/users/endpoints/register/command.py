from django.db import IntegrityError
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

from apps.users.tokens import issue_tokens

User = get_user_model()


class RegisterCommand:
    def execute(self, email, password, first_name="", last_name=""):
        try:
            user = User.objects.create_user(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
            )
        except IntegrityError:
            raise ValidationError({"email": ["A user with this email already exists."]})
        return issue_tokens(user)
