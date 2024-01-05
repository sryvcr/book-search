import pytest
from django.urls import reverse
from rest_framework import status

from apps.library_admin.constants import (
    GOOGLE_BOOKS_API_SOURCE, INTERNAL_SOURCE
)
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
class TestBookAPIView:
    def setup_method(self):
        self.url = reverse("books_api_v1")

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

    def test_get__all_internal_books(self, api_client):
        response = api_client.get(self.url)
        response_json = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert len(response_json) == 2

    def test_get__search_internal_books_by_title(self, api_client):
        SEARCH_BY_TITLE = "Architecture"
        query_params = {
            "search": SEARCH_BY_TITLE
        }

        response = api_client.get(self.url, query_params)
        response_json = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert len(response_json) == 1
        assert response_json[0]["title"] == self.book_2.title
        assert response_json[0]["subtitle"] == self.book_2.subtitle
        assert len(response_json[0]["authors"]) == len(self.book_2.authors)
        assert len(response_json[0]["categories"]) == len(self.book_2.categories)
        assert response_json[0]["publication_date"] == self.book_2.publication_date
        assert response_json[0]["editor"] == self.book_2.editor
        assert response_json[0]["description"] == self.book_2.description
        assert response_json[0]["image"] == self.book_2.image
        assert response_json[0]["source"] == INTERNAL_SOURCE

    def test_get__search_internal_books_by_subtitle(self, api_client):
        SEARCH_BY_SUBTITLE = "An Insider's"
        query_params = {
            "search": SEARCH_BY_SUBTITLE
        }

        response = api_client.get(self.url, query_params)
        response_json = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert len(response_json) == 1
        assert response_json[0]["title"] == self.book_1.title
        assert response_json[0]["subtitle"] == self.book_1.subtitle
        assert len(response_json[0]["authors"]) == len(self.book_1.authors)
        assert len(response_json[0]["categories"]) == len(self.book_1.categories)
        assert response_json[0]["publication_date"] == self.book_1.publication_date
        assert response_json[0]["editor"] == self.book_1.editor
        assert response_json[0]["description"] == self.book_1.description
        assert response_json[0]["image"] == self.book_1.image
        assert response_json[0]["source"] == INTERNAL_SOURCE

    def test_get__search_internal_books_by_author(self, api_client):
        SEARCH_BY_AUTHOR = "Alex"
        query_params = {
            "search": SEARCH_BY_AUTHOR
        }

        response = api_client.get(self.url, query_params)
        response_json = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert len(response_json) == 1
        assert response_json[0]["title"] == self.book_1.title
        assert response_json[0]["subtitle"] == self.book_1.subtitle
        assert len(response_json[0]["authors"]) == len(self.book_1.authors)
        assert len(response_json[0]["categories"]) == len(self.book_1.categories)
        assert response_json[0]["publication_date"] == self.book_1.publication_date
        assert response_json[0]["editor"] == self.book_1.editor
        assert response_json[0]["description"] == self.book_1.description
        assert response_json[0]["image"] == self.book_1.image
        assert response_json[0]["source"] == INTERNAL_SOURCE

    def test_get__search_internal_books_by_category(self, api_client):
        SEARCH_BY_AUTHOR = "Web"
        query_params = {
            "search": SEARCH_BY_AUTHOR
        }

        response = api_client.get(self.url, query_params)
        response_json = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert len(response_json) == 2

    @pytest.mark.parametrize(
        "publication_date", ["2017-09-10", "2017-09", "2017-09"]
    )
    def test_get__search_internal_books_by_publication_date(
        self, api_client, publication_date
    ):
        query_params = {
            "search": publication_date
        }

        response = api_client.get(self.url, query_params)
        response_json = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert len(response_json) == 1
        assert response_json[0]["title"] == self.book_2.title

    def test_get__search_internal_books_by_editor(self, api_client):
        SEARCH_BY_EDITOR = "Byte"
        query_params = {
            "search": SEARCH_BY_EDITOR
        }

        response = api_client.get(self.url, query_params)
        response_json = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert len(response_json) == 1
        assert response_json[0]["title"] == self.book_1.title

    def test_post__create_book_from_google_api(self, api_client):
        GOOGLE_BOOK_ID = "_i6bDeoCQzsC"
        payload = {
            "id": GOOGLE_BOOK_ID,
            "source": GOOGLE_BOOKS_API_SOURCE
        }

        response = api_client.post(self.url, payload)

        assert response.status_code == status.HTTP_201_CREATED

    def test_post__book_already_exists(self, api_client):
        GOOGLE_BOOK_ID = "uGE1DwAAQBAJ"
        payload = {
            "id": GOOGLE_BOOK_ID,
            "source": GOOGLE_BOOKS_API_SOURCE
        }

        response = api_client.post(self.url, payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestBookDetailAPIView:
    def setup_method(self):
        self.author = author_robert_martin.make()

        self.category = category_web_development.make()

        self.book = book_clean_architecture.make()
        self.book.author.add(self.author)
        self.book.category.add(self.category)

    def test_delete_book(self, api_client):
        URL = reverse("book_details_api_v1", kwargs={"pk": self.book.id})
        response = api_client.delete(URL)

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete__book_does_not_exists(self, api_client):
        URL = reverse("book_details_api_v1", kwargs={"pk": 987654321})
        response = api_client.delete(URL)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
