import pytest
from asgiref.sync import async_to_sync

from apps.library_admin.exceptions import AuthorDoesNotExist
from apps.library_admin.models import Author
from apps.library_admin.providers import author as author_providers
from apps.library_admin.tests.recipes import (
    author_alex_xu,
    author_sahn_lam,
    book_system_design_interview,
)


@pytest.mark.django_db
class TestGetBookAuthorNamesByBookId:
    def setup_method(self):
        self.book = book_system_design_interview.make()
        self.author_1 = author_alex_xu.make()
        self.author_2 = author_sahn_lam.make()

        self.book.author.add(self.author_1)
        self.book.author.add(self.author_2)

    def test_get_book_authors(self):
        result = async_to_sync(author_providers.get_book_author_names_by_book_id)(
            book_id=self.book.id
        )

        assert len(result) == 2
        assert self.book.authors[0].name in result
        assert self.book.authors[1].name in result

    def test_no_book_authors(self):
        FAKE_BOOK_ID = 101001010111
        result = async_to_sync(author_providers.get_book_author_names_by_book_id)(
            book_id=FAKE_BOOK_ID
        )

        assert len(result) == 0


@pytest.mark.django_db
class TestGetAuthorByAuthorName:
    def setup_method(self):
        self.author = author_alex_xu.make()

    def test_get_author(self):
        result = async_to_sync(author_providers.get_author_by_author_name)(
            author_name=self.author.name
        )

        assert isinstance(result, Author)
        assert result.id == self.author.id
        assert result.name == self.author.name

    def test_raise_author_does_not_exist(self):
        FAKE_AUTHOR_NAME = "Fake Author Name"
        with pytest.raises(expected_exception=AuthorDoesNotExist):
            async_to_sync(author_providers.get_author_by_author_name)(
                author_name=FAKE_AUTHOR_NAME
            )


@pytest.mark.django_db
def test_create_author():
    AUTHOR_NAME = "Author Name"
    result = async_to_sync(author_providers.create_author)(name=AUTHOR_NAME)

    assert isinstance(result, Author)
    assert result.name == AUTHOR_NAME
