from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken


class RefreshCommand:
    def execute(self, refresh):
        try:
            token = RefreshToken(refresh)
        except TokenError:
            raise AuthenticationFailed("Invalid or expired refresh token.")
        return {"access": str(token.access_token)}
