from rest_framework import status
from rest_framework.response import Response


class BaseErrorResponse(Response):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    def __init__(self, error_msg: str = "API_INTERNAL_ERROR"):
        self.error = error_msg
        data = {
            "error": self.error,
        }

        super().__init__(data=data, status=self.status_code)


class BookAlreadyExistsResponse(BaseErrorResponse):
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, error_msg: str = "BOOK_ALREADY_EXISTS_ERROR"):
        self.error = error_msg
        data = {
            "error": self.error,
        }

        super(BaseErrorResponse, self).__init__(data=data, status=self.status_code)


class BookDoesNotExistResponse(BaseErrorResponse):
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, error_msg: str = "BOOK_DOES_NOT_EXIST_ERROR"):
        self.error = error_msg
        data = {
            "error": self.error,
        }

        super(BaseErrorResponse, self).__init__(data=data, status=self.status_code)
