import pytest
from asgiref.sync import async_to_sync

from apps.library_admin.exceptions import CategoryDoesNotExist
from apps.library_admin.models import Category
from apps.library_admin.providers import category as category_providers
from apps.library_admin.tests.recipes import (
    book_system_design_interview,
    category_computer,
    category_web_development,
)


@pytest.mark.django_db
class TestGetBookCategoryNamesByBookId:
    def setup_method(self):
        self.book = book_system_design_interview.make()
        self.category_1 = category_computer.make()
        self.category_2 = category_web_development.make()

        self.book.category.add(self.category_1)
        self.book.category.add(self.category_2)

    def test_get_book_categories(self):
        result = async_to_sync(category_providers.get_book_category_names_by_book_id)(
            book_id=self.book.id
        )

        assert len(result) == 2
        assert self.book.categories[0].name in result
        assert self.book.categories[1].name in result

    def test_no_book_categories(self):
        FAKE_BOOK_ID = 101001010111
        result = async_to_sync(category_providers.get_book_category_names_by_book_id)(
            book_id=FAKE_BOOK_ID
        )

        assert len(result) == 0


@pytest.mark.django_db
class TestGetCategoryByCategoryName:
    def setup_method(self):
        self.category = category_web_development.make()

    def test_get_category(self):
        result = async_to_sync(category_providers.get_category_by_category_name)(
            category_name=self.category.name
        )

        assert isinstance(result, Category)
        assert result.id == self.category.id
        assert result.name == self.category.name

    def test_raise_category_does_not_exist(self):
        FAKE_CATEGORY_NAME = "Fake Category Name"
        with pytest.raises(expected_exception=CategoryDoesNotExist):
            async_to_sync(category_providers.get_category_by_category_name)(
                category_name=FAKE_CATEGORY_NAME
            )


@pytest.mark.django_db
def test_create_category():
    CATEGORY_NAME = "Category Name"
    result = async_to_sync(category_providers.create_category)(name=CATEGORY_NAME)

    assert isinstance(result, Category)
    assert result.name == CATEGORY_NAME
