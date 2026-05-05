from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        response.data = {
            "error":  True,
            "status_code": response.status_code,
            "detail": response.data
        }
    
    return response


class ServiceException(Exception):
    """Raised by service layer when a business rule is violated."""
    def __init__(self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        self.message = message
        self.status_code = status_code
        super().__init__(message)
        