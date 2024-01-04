from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

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
            )

        books_serializer = BookSerializer(books, many=True)

        return Response(books_serializer.data, status=status.HTTP_200_OK)
