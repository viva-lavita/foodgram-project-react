from django.http import Http404
from rest_framework.views import exception_handler
from rest_framework.response import Response


def custom_exception_handler(exc, context) -> Response:
    response = exception_handler(exc, context)

    if isinstance(exc, Http404):
        return Response(
            {'detail': 'Запрашиваемый объект не найден'},
            status=404
        )

    return response
