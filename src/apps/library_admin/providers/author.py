from django.db.models import QuerySet

from apps.library_admin.models import Author


def get_book_author_names_by_book_id(book_id: int) -> QuerySet:
    return Author.objects.filter(book__id=book_id).values_list("name", flat=True)
