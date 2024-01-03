from django.urls import re_path

from apps.library_admin.views import BookAPIView


urlpatterns = [
    re_path(
        r"^v1/", BookAPIView.as_view(), name="books_api_v1",
    ),
]
