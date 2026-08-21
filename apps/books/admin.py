from django.contrib import admin

from apps.books.models import Book, Review


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author_name", "isbn", "created_at")
    search_fields = ("title", "author_name", "isbn")
    list_filter = ("created_at",)
    readonly_fields = ("created_at", "updated_at")
    ordering = ("title",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("book", "user", "rating", "created_at")
    list_filter = ("rating", "created_at")
    search_fields = ("comment", "user__email", "book__title")
    autocomplete_fields = ("user", "book")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)
