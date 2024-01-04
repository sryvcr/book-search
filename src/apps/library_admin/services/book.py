from apps.utils import build_dataclass_from_model_instance
from apps.library_admin import constants as library_admin_constants
from apps.library_admin.dataclasses import BookDataclass
from apps.library_admin.providers import author as author_providers
from apps.library_admin.providers import book as book_providers
from apps.library_admin.providers import category as category_providers


def get_books() -> list[BookDataclass]:
    books = book_providers.get_books()

    return [
        build_dataclass_from_model_instance(
            klass=BookDataclass,
            instance=book,
            authors=author_providers.get_book_author_names_by_book_id(book_id=book.id),
            categories=category_providers.get_book_category_names_by_book_id(
                book_id=book.id
            ),
            source=library_admin_constants.INTERNAL_SOURCE,
        ) for book in books
    ]


def get_books_by_search_parameter(search: str) -> list[BookDataclass]:
    books = book_providers.get_books_by_search_parameter(search=search)

    return [
        build_dataclass_from_model_instance(
            klass=BookDataclass,
            instance=book,
            authors=author_providers.get_book_author_names_by_book_id(book_id=book.id),
            categories=category_providers.get_book_category_names_by_book_id(
                book_id=book.id
            ),
            source=library_admin_constants.INTERNAL_SOURCE,
        ) for book in books
    ]
