from django.db import transaction
from datetime import datetime

from apps.utils import build_dataclass_from_model_instance
from apps.library_admin import constants as library_admin_constants
from apps.library_admin.dataclasses import BookDataclass
from apps.library_admin.providers import author as author_providers
from apps.library_admin.providers import book as book_providers
from apps.library_admin.providers import category as category_providers
from apps.library_admin.services import (
    third_party_book_apis as third_party_book_apis_service
)
from apps.library_admin.exceptions import (
    BookAlreadyCreated, BookDoesNotExist, AuthorDoesNotExist, CategoryDoesNotExist
)


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


def create_book_from_external_source(book_id: str, source: str) -> BookDataclass | None:
    match source:
        case library_admin_constants.GOOGLE_BOOKS_API_SOURCE:
            book = third_party_book_apis_service.get_book_from_google_api_by_id(
                book_id=book_id
            )
            if book:
                try:
                    return create_book_from_google_book_api(book=book)
                except BookAlreadyCreated as err:
                    raise err
        case _:
            return None


def create_book_from_google_book_api(book: BookDataclass) -> BookDataclass:
    if not book_providers.check_if_book_exists_by_title(book_title=book.title):
        authors = []
        categories = []

        with transaction.atomic():
            for author in book.authors:
                try:
                    author = author_providers.get_author_by_author_name(
                        author_name=author
                    )
                    authors.append(author)
                except AuthorDoesNotExist:
                    author = author_providers.create_author(name=author)
                    authors.append(author)

            for category in book.categories:
                try:
                    category = category_providers.get_category_by_category_name(
                        author_name=author
                    )
                    categories.append(category)
                except CategoryDoesNotExist:
                    category = category_providers.create_category(name=category)
                    categories.append(category)

            book.publication_date = __validate_and_return_correct_publication_date_format(
                publication_date=book.publication_date
            )

            new_book = book_providers.create_book(book=book)

            if authors:
                new_book.author.set(authors)

            if categories:
                new_book.category.set(categories)

        return build_dataclass_from_model_instance(
            klass=BookDataclass,
            instance=new_book,
            authors=author_providers.get_book_author_names_by_book_id(
                book_id=new_book.id
            ),
            categories=category_providers.get_book_category_names_by_book_id(
                book_id=new_book.id
            ),
            source=library_admin_constants.INTERNAL_SOURCE,
        )
    else:
        raise BookAlreadyCreated(book_title=book.title)


def __validate_and_return_correct_publication_date_format(publication_date: str):
    PUBLICATION_DATE_FORMAT = "%Y-%m-%d"
    DEFAULT_PUBLICATION_DATE = "1800-01-01"
    try:
        return datetime.strptime(publication_date, PUBLICATION_DATE_FORMAT)
    except ValueError:
        return datetime.strptime(DEFAULT_PUBLICATION_DATE, PUBLICATION_DATE_FORMAT)


def delete_book(book_id: int) -> bool:
    try:
        return book_providers.delete_book(book_id=book_id)
    except BookDoesNotExist as err:
        raise err
