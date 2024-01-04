import pytest
from unittest import mock

from apps.library_admin.exceptions import AuthorDoesNotExist
from apps.library_admin.models import Author
from apps.library_admin.providers import author as author_providers
from apps.library_admin.tests.recipes import (
    author_alex_xu,
    book_system_design_interview,
)


@pytest.mark.django_db
class TestGetBookAuthorNamesByBookId:
    def setup_method(self):
        self.book = book_system_design_interview.make()

    def test_get_book_authors(self):
        result = author_providers.get_book_author_names_by_book_id(book_id=self.book.id)

        assert len(result) == 2
        assert self.book.authors[0].name in result
        assert self.book.authors[1].name in result

    def test_no_book_authors(self):
        FAKE_BOOK_ID = 101001010111
        result = author_providers.get_book_author_names_by_book_id(book_id=FAKE_BOOK_ID)

        assert len(result) == 0


@pytest.mark.django_db
class TestGetAuthorByAuthorName:
    def setup_method(self):
        self.author = author_alex_xu.make()

    def test_get_author(self):
        result = author_providers.get_author_by_author_name(
            author_name=self.author.name
        )

        assert isinstance(result, Author)
        assert result.id == self.author.id
        assert result.name == self.author.name

    def test_raise_author_does_not_exist(self):
        FAKE_AUTHOR_NAME = "Fake Author Name"
        with pytest.raises(expected_exception=AuthorDoesNotExist):
            author_providers.get_author_by_author_name(author_name=FAKE_AUTHOR_NAME)
