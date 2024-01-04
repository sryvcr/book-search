from django.db.models import Q, QuerySet

from apps.library_admin.dataclasses import BookDataclass
from apps.library_admin.exceptions import BookDoesNotExist
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


def check_if_book_exists_by_title(book_title: str) -> bool:
    return Book.objects.filter(title=book_title).exists()


def create_book(book: Book | BookDataclass) -> Book:
    return Book.objects.create(
        title=book.title,
        subtitle=book.subtitle,
        publication_date=book.publication_date,
        editor=book.editor,
        description=book.description,
        image=book.image,
    )


def delete_book(book_id: int) -> bool:
    try:
        Book.objects.get(id=book_id).delete()
        return True
    except Book.DoesNotExist:
        raise BookDoesNotExist()
