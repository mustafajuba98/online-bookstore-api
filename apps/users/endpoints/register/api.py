from rest_framework import status
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from apps.common.throttles import AuthRateThrottle
from apps.users.endpoints.register.command import RegisterCommand
from apps.users.serializers import AuthTokensSerializer, RegisterSerializer


@extend_schema(
    auth=None,
    request=RegisterSerializer,
    responses={201: AuthTokensSerializer},
)
@api_view(["POST"])
@throttle_classes([AuthRateThrottle])
def register_api(request):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    result = RegisterCommand().execute(**serializer.validated_data)
    return Response(AuthTokensSerializer(result).data, status=status.HTTP_201_CREATED)
