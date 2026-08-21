from drf_spectacular.utils import OpenApiParameter, extend_schema, inline_serializer
from rest_framework import serializers, status
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from apps.books.endpoints.reviews.command import ListReviewsCommand, SubmitReviewCommand
from apps.books.serializers import ReviewSerializer, ReviewWriteSerializer


@extend_schema(
    methods=["GET"],
    parameters=[OpenApiParameter("page", int, OpenApiParameter.QUERY)],
    responses={
        200: inline_serializer(
            name="PaginatedReviewList",
            fields={
                "count": serializers.IntegerField(),
                "next": serializers.URLField(allow_null=True),
                "previous": serializers.URLField(allow_null=True),
                "results": ReviewSerializer(many=True),
            },
        )
    },
)
@extend_schema(
    methods=["POST"],
    request=ReviewWriteSerializer,
    responses={201: ReviewSerializer},
)
@api_view(["GET", "POST"])
def reviews_api(request, book_id):
    if request.method == "POST":
        serializer = ReviewWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        review = SubmitReviewCommand().execute(
            user=request.user,
            book_id=book_id,
            **serializer.validated_data,
        )
        return Response(ReviewSerializer(review).data, status=status.HTTP_201_CREATED)

    queryset = ListReviewsCommand().execute(book_id)
    paginator = PageNumberPagination()
    page = paginator.paginate_queryset(queryset, request)
    return paginator.get_paginated_response(ReviewSerializer(page, many=True).data)
