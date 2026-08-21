from rest_framework.decorators import api_view, throttle_classes
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from apps.common.throttles import AuthRateThrottle
from apps.users.endpoints.refresh.command import RefreshCommand
from apps.users.serializers import AccessTokenSerializer, RefreshSerializer


@extend_schema(
    auth=None,
    request=RefreshSerializer,
    responses={200: AccessTokenSerializer},
)
@api_view(["POST"])
@throttle_classes([AuthRateThrottle])
def refresh_api(request):
    serializer = RefreshSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    result = RefreshCommand().execute(**serializer.validated_data)
    return Response(AccessTokenSerializer(result).data)
