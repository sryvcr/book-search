from django.db.models import Q, QuerySet

from apps.library_admin.models import Book


def get_books() -> QuerySet:
    return Book.objects.all()


def get_books_by_search_parameter(search: str) -> QuerySet:
    return Book.objects.filter(
        Q(title__icontains=search)
        | Q(subtitle__icontains=search)
        | Q(author__name__icontains=search)
        | Q(category__name__icontains=search)
        | Q(publication_date__icontains=search)
        | Q(editor__icontains=search)
    ).distinct()
