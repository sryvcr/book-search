from django.db.models import QuerySet

from apps.library_admin.models import Author
from apps.library_admin.exceptions import AuthorDoesNotExist


def get_book_author_names_by_book_id(book_id: int) -> QuerySet:
    return (
        Author.objects.filter(book__id=book_id)
        .order_by("name")
        .values_list("name", flat=True)
    )


def get_author_by_author_name(author_name: str) -> bool:
    try:
        return Author.objects.get(name=author_name)
    except Author.DoesNotExist:
        raise AuthorDoesNotExist()


def create_author(name: str):
    return Author.objects.create(name=name)
