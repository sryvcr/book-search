from django.db.models import QuerySet

from apps.library_admin.models import Category


def get_book_category_names_by_book_id(book_id: int) -> QuerySet:
    return Category.objects.filter(book__id=book_id).values_list("name", flat=True)
