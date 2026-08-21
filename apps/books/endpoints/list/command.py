from django.db.models import Count, Q

from apps.books.models import Book


class ListBooksCommand:
    def execute(self, search=None):
        queryset = Book.objects.defer("content").annotate(reviews_count=Count("reviews"))
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(author_name__icontains=search)
            )
        return queryset
