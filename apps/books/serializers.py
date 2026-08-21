from rest_framework import serializers

from apps.books.models import Book


class BookListSerializer(serializers.ModelSerializer):
    reviews_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Book
        fields = (
            "id",
            "title",
            "author_name",
            "description",
            "isbn",
            "reviews_count",
            "created_at",
        )


class BookDetailSerializer(serializers.ModelSerializer):
    reviews_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Book
        fields = (
            "id",
            "title",
            "author_name",
            "description",
            "content",
            "isbn",
            "reviews_count",
            "created_at",
            "updated_at",
        )
