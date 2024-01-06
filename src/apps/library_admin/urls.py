from django.urls import re_path

from apps.library_admin.views import BookAPIView, BookDetailAPIView


urlpatterns = [
    re_path(
        r"^v1/?$",
        BookAPIView.as_view(),
        name="books_api_v1",
    ),
    re_path(
        r"^v1/(?P<pk>\d+)/?$",
        BookDetailAPIView.as_view(),
        name="book_details_api_v1",
    ),
]
