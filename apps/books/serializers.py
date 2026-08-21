from rest_framework import serializers

from apps.books.models import Book, Review
from apps.users.serializers import UserSerializer


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


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ("id", "user", "rating", "comment", "created_at", "updated_at")


class ReviewWriteSerializer(serializers.Serializer):
    rating = serializers.IntegerField(min_value=1, max_value=5)
    comment = serializers.CharField(min_length=1, max_length=5000)
