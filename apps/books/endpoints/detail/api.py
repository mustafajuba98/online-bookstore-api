from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.books.endpoints.detail.command import GetBookCommand
from apps.books.serializers import BookDetailSerializer


@extend_schema(responses={200: BookDetailSerializer, 404: None})
@api_view(["GET"])
def get_book_api(request, book_id):
    book = GetBookCommand().execute(book_id)
    return Response(BookDetailSerializer(book).data)
