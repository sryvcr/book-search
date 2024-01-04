from apps.utils import build_dataclass_from_dict, get_json_response_from_get_request
from apps.library_admin import constants as library_admin_constants
from apps.library_admin.dataclasses import BookDataclass



GOOGLE_BOOK_API_BASE_URL = "https://www.googleapis.com/books/v1/volumes"


def get_book_from_google_api_by_search_parameter(search: str) -> list[BookDataclass]:
    books = []

    json_response = get_json_response_from_get_request(
        url=f"{GOOGLE_BOOK_API_BASE_URL}?q={search}"
    )

    if "items" in json_response:
        for item in json_response["items"]:
            title = item["volumeInfo"]["title"]

            try:
                subtitle = item["volumeInfo"]["subtitle"]
            except KeyError:
                subtitle = ""

            try:
                authors = item["volumeInfo"]["authors"]
            except KeyError:
                authors = ""

            try:
                categories = item["categories"]
            except KeyError:
                categories = ""

            try:
                editor = item["volumeInfo"]["publisher"]
            except KeyError:
                editor = ""

            try:
                publication_date = item["volumeInfo"]["publishedDate"]
            except KeyError:
                publication_date = ""

            try:
                description = item["volumeInfo"]["description"]
            except KeyError:
                description = ""

            try:
                image = item["imageLinks"]["thumbnail"]
            except KeyError:
                image = ""

            books.append(
                build_dataclass_from_dict(
                    klass=BookDataclass,
                    data=item,
                    title=title,
                    subtitle=subtitle,
                    authors=authors,
                    categories=categories,
                    publication_date=publication_date,
                    editor=editor,
                    description=description,
                    image=image,
                    source=library_admin_constants.GOOGLE_BOOKS_API_SOURCE,
                )
            )

    return books
