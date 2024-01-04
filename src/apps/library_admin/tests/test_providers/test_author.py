import pytest
from unittest import mock

from apps.library_admin.providers import author as author_providers
from apps.library_admin.tests.recipes import book_system_design_interview


@pytest.mark.django_db
class TestGetBookAuthorNamesByBookId():
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
