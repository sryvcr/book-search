from django.core.exceptions import ObjectDoesNotExist


class AuthorDoesNotExist(ObjectDoesNotExist):
    pass


class CategoryDoesNotExist(ObjectDoesNotExist):
    pass


class BookAlreadyCreated(Exception):
    pass
