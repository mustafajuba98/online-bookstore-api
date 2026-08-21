from rest_framework.authentication import BaseAuthentication


class MiddlewareJWTAuthentication(BaseAuthentication):
    """Use the user already set by JWTAuthenticationMiddleware."""

    def authenticate(self, request):
        user = getattr(request._request, "user", None)
        if user is not None and user.is_authenticated:
            return (user, None)
        return None

    def authenticate_header(self, request):
        return "Bearer"
