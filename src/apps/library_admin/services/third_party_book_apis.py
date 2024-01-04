from apps.utils import build_dataclass_from_dict, get_json_response_from_get_request
from apps.library_admin import constants as library_admin_constants
from apps.library_admin.dataclasses import BookDataclass



GOOGLE_BOOK_API_BASE_URL = "https://www.googleapis.com/books/v1/volumes"


def get_book_from_google_api_by_search_parameter(search: str) -> list[BookDataclass]:
    books = []

    json_response = get_json_response_from_get_request(
        url=GOOGLE_BOOK_API_BASE_URL, params={"q": search}
    )

    if "items" in json_response:
        for item in json_response["items"]:
            books.append(
                __build_book_dataclass_from_google_books_api_data(book_data=item)
            )

    return books


def __build_book_dataclass_from_google_books_api_data(
    book_data: dict
) -> BookDataclass:
    title = book_data["volumeInfo"]["title"]

    try:
        subtitle = book_data["volumeInfo"]["subtitle"]
    except KeyError:
        subtitle = ""

    try:
        authors = book_data["volumeInfo"]["authors"]
    except KeyError:
        authors = []

    try:
        categories = book_data["categories"]
    except KeyError:
        categories = []

    try:
        editor = book_data["volumeInfo"]["publisher"]
    except KeyError:
        editor = ""

    try:
        publication_date = book_data["volumeInfo"]["publishedDate"]
    except KeyError:
        publication_date = ""

    try:
        description = book_data["volumeInfo"]["description"]
    except KeyError:
        description = ""

    try:
        image = book_data["imageLinks"]["thumbnail"]
    except KeyError:
        image = ""

    return (
        build_dataclass_from_dict(
            klass=BookDataclass,
            data=book_data,
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


def get_book_from_google_api_by_id(book_id: str) -> BookDataclass:
    book_data = get_json_response_from_get_request(
        url=f"{GOOGLE_BOOK_API_BASE_URL}/{book_id}", params={}
    )

    return __build_book_dataclass_from_google_books_api_data(book_data=book_data)
