import pytest
from asgiref.sync import async_to_sync

from apps.library_admin.constants import INTERNAL_SOURCE
from apps.library_admin.dataclasses import BookDataclass
from apps.library_admin.exceptions import BookDoesNotExist
from apps.library_admin.services import book as book_services
from apps.library_admin.tests.recipes import (
    author_alex_xu,
    author_sahn_lam,
    author_robert_martin,
    book_clean_architecture,
    book_system_design_interview,
    category_web_development,
    category_computer,
)


@pytest.mark.django_db
def test_get_books():
    book_1 = book_clean_architecture.make()

    result = async_to_sync(book_services.get_books)()

    assert len(result) == 1
    assert isinstance(result[0], BookDataclass)
    assert result[0].title == book_1.title
    assert result[0].subtitle == book_1.subtitle
    assert len(result[0].authors) == 0
    assert len(result[0].categories) == 0
    assert str(result[0].publication_date) == book_1.publication_date
    assert result[0].editor == book_1.editor
    assert result[0].description == book_1.description
    assert result[0].image == book_1.image
    assert result[0].source == INTERNAL_SOURCE


@pytest.mark.django_db
class TestGetBooksBySearchParameter:
    def setup_method(self):
        self.author_1 = author_alex_xu.make()
        self.author_2 = author_sahn_lam.make()
        self.author_3 = author_robert_martin.make()

        self.category_1 = category_computer.make()
        self.category_2 = category_web_development.make()

        self.book_1 = book_system_design_interview.make()
        self.book_1.author.add(self.author_1)
        self.book_1.author.add(self.author_2)
        self.book_1.category.add(self.category_1)
        self.book_1.category.add(self.category_2)

        self.book_2 = book_clean_architecture.make()
        self.book_2.author.add(self.author_3)
        self.book_2.category.add(self.category_2)

    def test_get_books_by_title(self):
        SEARCH_BY_TITLE = "System"
        result = async_to_sync(book_services.get_books_by_search_parameter)(
            search=SEARCH_BY_TITLE
        )

        assert len(result) == 1
        assert isinstance(result[0], BookDataclass)
        assert result[0].title == self.book_1.title
        assert len(result[0].authors) == 2
        assert len(result[0].categories) == 2

    def test_get_books_by_subtitle(self):
        SEARCH_BY_SUBTITLE = "A Craftsman's Guide"
        result = async_to_sync(book_services.get_books_by_search_parameter)(
            search=SEARCH_BY_SUBTITLE
        )

        assert len(result) == 1
        assert isinstance(result[0], BookDataclass)
        assert result[0].title == self.book_2.title
        assert result[0].subtitle == self.book_2.subtitle
        assert len(result[0].authors) == 1
        assert len(result[0].categories) == 1

    def test_get_books_by_author(self):
        SEARCH_BY_AUTHOR = "Alex"
        result = async_to_sync(book_services.get_books_by_search_parameter)(
            search=SEARCH_BY_AUTHOR
        )

        assert len(result) == 1
        assert isinstance(result[0], BookDataclass)
        assert result[0].title == self.book_1.title
        assert len(result[0].authors) == 2
        assert len(result[0].categories) == 2

    def test_get_books_by_category(self):
        SEARCH_BY_CATEGORY = "Web"
        result = async_to_sync(book_services.get_books_by_search_parameter)(
            search=SEARCH_BY_CATEGORY
        )

        assert len(result) == 2
        assert isinstance(result[0], BookDataclass)
        assert isinstance(result[1], BookDataclass)

    @pytest.mark.parametrize("publication_date", ["2020-02-12", "2020-02", "2020"])
    def test_get_books_by_publication_date(self, publication_date):
        result = async_to_sync(book_services.get_books_by_search_parameter)(
            search=publication_date
        )

        assert len(result) == 1
        assert isinstance(result[0], BookDataclass)
        assert result[0].title == self.book_1.title


@pytest.mark.django_db
@pytest.mark.asyncio
class TestDeleteBook:
    async def test_delete_book(self, book_system_design_interview_async):
        result = await book_services.delete_book(
            book_id=book_system_design_interview_async.id
        )

        assert result is True

    async def test_delete_book__does_not_exist_exception(
        self, book_system_design_interview_async
    ):
        FAKE_BOOK_ID = 9876543210
        with pytest.raises(BookDoesNotExist):
            await book_services.delete_book(book_id=FAKE_BOOK_ID)
