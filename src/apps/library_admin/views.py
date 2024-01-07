import asyncio
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from adrf.views import APIView

from apps.library_admin.exceptions import BookAlreadyCreated, BookDoesNotExist
from apps.library_admin.responses.error import (
    BookAlreadyExistsResponse,
    BookDoesNotExistResponse,
)
from apps.library_admin.services import book as book_services
from apps.library_admin.services import third_party_book_apis as book_apis_services
from apps.library_admin.serializers import BookSerializer


class BookAPIView(APIView):
    def get(self, request: Request) -> Response:
        search = request.query_params.get("search")

        if not search:
            books = book_services.get_books()
        else:
            books = book_services.get_books_by_search_parameter(search=search)

        if not books:
            books = book_apis_services.get_book_from_google_api_by_search_parameter(
                search=search
            ) or book_apis_services.get_books_from_open_library_by_search_parameter(
                search=search
            )

        books_serializer = BookSerializer(books, many=True)

        return Response(books_serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        book_id = request.data.get("id")
        source = request.data.get("source")

        try:
            book = book_services.create_book_from_external_source(
                book_id=book_id, source=source
            )
        except BookAlreadyCreated as err:
            return BookAlreadyExistsResponse(error_msg=err.msg)

        serializer = BookSerializer(book)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class BookDetailAPIView(APIView):
    async def delete(self, request: Request, pk: int) -> Response:
        try:
            await asyncio.gather(book_services.delete_book(book_id=pk))
            return Response(status=status.HTTP_204_NO_CONTENT)
        except BookDoesNotExist:
            return BookDoesNotExistResponse()
