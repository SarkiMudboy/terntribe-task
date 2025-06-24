from rest_framework.exceptions import APIException


class ResourceNotFoundException(APIException):
    """For raising HTTP_404 Exception"""

    status_code = 404
    default_detail = "Not Found"
    default_code = "not_found"
