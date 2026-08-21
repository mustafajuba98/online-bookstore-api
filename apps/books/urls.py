from django.urls import path

from apps.books.endpoints.detail.api import get_book_api
from apps.books.endpoints.list.api import list_books_api

urlpatterns = [
    path("books/", list_books_api, name="book-list"),
    path("books/<int:book_id>/", get_book_api, name="book-detail"),
]
