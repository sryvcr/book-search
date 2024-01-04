from django.core.exceptions import ObjectDoesNotExist


class AuthorDoesNotExist(ObjectDoesNotExist):
    pass


class CategoryDoesNotExist(ObjectDoesNotExist):
    pass


class BookAlreadyCreated(Exception):
    def __init__(self, book_title: str, msg=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.book_title = book_title
        self.msg = msg or f"The book '{book_title}' is already created"
