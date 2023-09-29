from http import HTTPStatus

from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context) -> Response:
    response = exception_handler(exc, context)

    if isinstance(exc, Http404):
        return Response(
            {'detail': 'Запрашиваемый объект не найден'},
            status=HTTPStatus.NOT_FOUND
        )

    return response
