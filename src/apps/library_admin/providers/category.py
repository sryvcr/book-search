from django.db.models import QuerySet

from apps.library_admin.models import Category
from apps.library_admin.exceptions import CategoryDoesNotExist


def get_book_category_names_by_book_id(book_id: int) -> QuerySet:
    return Category.objects.filter(
        book__id=book_id
    ).order_by("name").values_list("name", flat=True)


def get_category_by_category_name(category_name: str) -> bool:
    try:
        return Category.objects.get(name=category_name)
    except Category.DoesNotExist:
        raise CategoryDoesNotExist()


def create_category(name: str):
    return Category.objects.create(name=name)
