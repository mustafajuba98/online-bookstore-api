from django.http import JsonResponse
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken


class JWTAuthenticationMiddleware:
    """Authenticate API requests from a Bearer access token."""

    PUBLIC_PREFIXES = (
        "/admin/",
        "/api/schema/",
        "/api/docs/",
        "/api/redoc/",
        "/api/auth/register/",
        "/api/auth/login/",
        "/api/auth/refresh/",
    )

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if self._is_public(request.path):
            return self.get_response(request)

        header = request.META.get("HTTP_AUTHORIZATION", "")
        if not header.startswith("Bearer "):
            return JsonResponse(
                {"detail": "Authentication credentials were not provided."},
                status=401,
            )

        User = get_user_model()
        try:
            token = AccessToken(header.split(" ", 1)[1])
            user = User.objects.get(pk=token["user_id"], is_active=True)
        except (TokenError, KeyError, User.DoesNotExist):
            return JsonResponse(
                {"detail": "Invalid or expired token."},
                status=401,
            )

        request.user = user
        return self.get_response(request)

    def _is_public(self, path):
        return any(path.startswith(prefix) for prefix in self.PUBLIC_PREFIXES)
