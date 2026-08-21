from django.contrib.auth import authenticate, get_user_model
from rest_framework.exceptions import AuthenticationFailed

from apps.users.tokens import issue_tokens

User = get_user_model()


class LoginCommand:
    def execute(self, email, password):
        email = User.objects.normalize_email(email)
        user = authenticate(username=email, password=password)
        if user is None:
            raise AuthenticationFailed("Invalid email or password.")
        return issue_tokens(user)
