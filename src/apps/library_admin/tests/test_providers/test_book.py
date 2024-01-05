import pytest

from apps.library_admin.models import Book
from apps.library_admin.providers import book as book_providers
from apps.library_admin.tests.recipes import (
    book_clean_architecture,
    book_system_design_interview,
)


@pytest.mark.django_db
def test_get_books():
    book_1 = book_system_design_interview.make()
    book_2 = book_clean_architecture.make()

    result = book_providers.get_books()

    assert len(result) == 2
    assert isinstance(result[0], Book)
    assert book_1 in result
    assert book_2 in result
