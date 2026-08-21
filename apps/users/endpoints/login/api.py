from rest_framework.decorators import api_view, throttle_classes
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from apps.common.throttles import AuthRateThrottle
from apps.users.endpoints.login.command import LoginCommand
from apps.users.serializers import AuthTokensSerializer, LoginSerializer


@extend_schema(
    auth=None,
    request=LoginSerializer,
    responses={200: AuthTokensSerializer},
)
@api_view(["POST"])
@throttle_classes([AuthRateThrottle])
def login_api(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    result = LoginCommand().execute(**serializer.validated_data)
    return Response(AuthTokensSerializer(result).data)
