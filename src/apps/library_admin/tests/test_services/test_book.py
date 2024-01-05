import pytest

from apps.library_admin.constants import INTERNAL_SOURCE
from apps.library_admin.dataclasses import BookDataclass
from apps.library_admin.services import book as book_services
from apps.library_admin.tests.recipes import book_clean_architecture


@pytest.mark.django_db
def test_get_books():
    book_1 = book_clean_architecture.make()

    result = book_services.get_books()

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
