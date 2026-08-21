from drf_spectacular.utils import OpenApiParameter, extend_schema, inline_serializer
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination

from apps.books.endpoints.list.command import ListBooksCommand
from apps.books.serializers import BookListSerializer


@extend_schema(
    parameters=[
        OpenApiParameter("page", int, OpenApiParameter.QUERY),
        OpenApiParameter("search", str, OpenApiParameter.QUERY),
    ],
    responses={
        200: inline_serializer(
            name="PaginatedBookList",
            fields={
                "count": serializers.IntegerField(),
                "next": serializers.URLField(allow_null=True),
                "previous": serializers.URLField(allow_null=True),
                "results": BookListSerializer(many=True),
            },
        )
    },
)
@api_view(["GET"])
def list_books_api(request):
    queryset = ListBooksCommand().execute(search=request.query_params.get("search"))
    paginator = PageNumberPagination()
    page = paginator.paginate_queryset(queryset, request)
    serializer = BookListSerializer(page, many=True)
    return paginator.get_paginated_response(serializer.data)
