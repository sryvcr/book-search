import pytest

from apps.library_admin.models import Book
from apps.library_admin.providers import book as book_providers
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
    book_1 = book_system_design_interview.make()
    book_2 = book_clean_architecture.make()

    result = book_providers.get_books()

    assert len(result) == 2
    assert isinstance(result[0], Book)
    assert book_1 in result
    assert book_2 in result


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
        result = book_providers.get_books_by_search_parameter(search=SEARCH_BY_TITLE)

        assert len(result) == 1
        assert isinstance(result[0], Book)
        assert result[0].title == self.book_1.title
        assert len(result[0].authors) == 2
        assert len(result[0].categories) == 2

    def test_get_books_by_subtitle(self):
        SEARCH_BY_SUBTITLE = "A Craftsman's Guide"
        result = book_providers.get_books_by_search_parameter(search=SEARCH_BY_SUBTITLE)

        assert len(result) == 1
        assert isinstance(result[0], Book)
        assert result[0].title == self.book_2.title
        assert result[0].subtitle == self.book_2.subtitle
        assert len(result[0].authors) == 1
        assert len(result[0].categories) == 1

    def test_get_books_by_author(self):
        SEARCH_BY_AUTHOR = "Alex"
        result = book_providers.get_books_by_search_parameter(search=SEARCH_BY_AUTHOR)

        assert len(result) == 1
        assert isinstance(result[0], Book)
        assert result[0].title == self.book_1.title
        assert len(result[0].authors) == 2
        assert len(result[0].categories) == 2

    def test_get_books_by_category(self):
        SEARCH_BY_CATEGORY = "Web"
        result = book_providers.get_books_by_search_parameter(search=SEARCH_BY_CATEGORY)

        assert len(result) == 2
        assert isinstance(result[0], Book)
        assert isinstance(result[1], Book)

    @pytest.mark.parametrize(
        "publication_date", ["2020-02-12", "2020-02", "2020"]
    )
    def test_get_books_by_publication_date(self, publication_date):
        result = book_providers.get_books_by_search_parameter(search=publication_date)

        assert len(result) == 1
        assert isinstance(result[0], Book)
        assert result[0].title == self.book_1.title


@pytest.mark.django_db
@pytest.mark.parametrize(
    ["book_title", "exists"],
    [
        ("Clean Architecture", True),
        ("Fake Title", False),
    ]
)
def test_check_if_book_exists_by_title(exists, book_title):
    book_clean_architecture.make()

    result = book_providers.check_if_book_exists_by_title(
        book_title=book_title
    )

    assert result == exists
