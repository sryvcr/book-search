from datetime import datetime

from apps.utils import build_dataclass_from_model_instance
from apps.library_admin import constants as library_admin_constants
from apps.library_admin.dataclasses import BookDataclass
from apps.library_admin.providers import author as author_providers
from apps.library_admin.providers import book as book_providers
from apps.library_admin.providers import category as category_providers
from apps.library_admin.services import (
    third_party_book_apis as third_party_book_apis_service,
)
from apps.library_admin.exceptions import (
    BookAlreadyCreated,
    BookDoesNotExist,
    AuthorDoesNotExist,
    CategoryDoesNotExist,
)


async def get_books() -> list[BookDataclass]:
    books = await book_providers.get_books()

    result = []
    async for book in books:
        authors = await author_providers.get_book_author_names_by_book_id(
            book_id=book.id
        )
        categories = await category_providers.get_book_category_names_by_book_id(
            book_id=book.id
        )
        book_dataclass = build_dataclass_from_model_instance(
            klass=BookDataclass,
            instance=book,
            authors=authors,
            categories=categories,
            source=library_admin_constants.INTERNAL_SOURCE,
        )
        result.append(book_dataclass)

    return result


async def get_books_by_search_parameter(search: str) -> list[BookDataclass]:
    books = await book_providers.get_books_by_search_parameter(search=search)

    result = []
    async for book in books:
        authors = await author_providers.get_book_author_names_by_book_id(
            book_id=book.id
        )
        categories = await category_providers.get_book_category_names_by_book_id(
            book_id=book.id
        )
        book_dataclass = build_dataclass_from_model_instance(
            klass=BookDataclass,
            instance=book,
            authors=authors,
            categories=categories,
            source=library_admin_constants.INTERNAL_SOURCE,
        )
        result.append(book_dataclass)

    return result


async def create_book_from_external_source(
    book_id: str, source: str
) -> BookDataclass | None:
    match source:
        case library_admin_constants.GOOGLE_BOOKS_API_SOURCE:
            book = await third_party_book_apis_service.get_book_from_google_api_by_id(
                book_id=book_id
            )
            if book:
                try:
                    return await create_book_from_google_book_api(book=book)
                except BookAlreadyCreated as err:
                    raise err
        case _:
            return None


async def create_book_from_google_book_api(book: BookDataclass) -> BookDataclass:
    if not await book_providers.check_if_book_exists_by_title(book_title=book.title):
        authors = []
        categories = []

        for author in book.authors:
            try:
                author = await author_providers.get_author_by_author_name(
                    author_name=author
                )
                authors.append(author)
            except AuthorDoesNotExist:
                author = await author_providers.create_author(name=author)
                authors.append(author)

        for category in book.categories:
            try:
                category = await category_providers.get_category_by_category_name(
                    category_name=category
                )
                categories.append(category)
            except CategoryDoesNotExist:
                category = await category_providers.create_category(name=category)
                categories.append(category)

        book.publication_date = __validate_and_return_correct_publication_date_format(
            publication_date=book.publication_date
        )

        new_book = await book_providers.create_book(book=book)

        if authors:
            await book_providers.add_authors_to_book(book=new_book, authors=authors)

        if categories:
            await book_providers.add_categories_to_book(
                book=new_book, categories=categories
            )

        authors = await author_providers.get_book_author_names_by_book_id(
            book_id=new_book.id
        )
        categories = await category_providers.get_book_category_names_by_book_id(
            book_id=new_book.id
        )

        return build_dataclass_from_model_instance(
            klass=BookDataclass,
            instance=new_book,
            authors=authors,
            categories=categories,
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


async def delete_book(book_id: int) -> bool:
    try:
        return await book_providers.delete_book(book_id=book_id)
    except BookDoesNotExist as err:
        raise err
