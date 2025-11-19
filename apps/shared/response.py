__all__ = [
    'ResponseFormat',
]

from django.utils.translation import gettext_lazy as trans

from rest_framework import status
from rest_framework.response import Response


class ResponseFormat:
    @staticmethod
    def failure_data_format(msg, status_code) -> dict:
        return {
            'message': msg,
            'status_code': status_code
        }

    @staticmethod
    def pagination(  # pylint: disable=R0917
            result, count, page_size,
            next_page, previous_page,
            status_code=status.HTTP_200_OK
    ):
        return Response(
            {
                'next': next_page,
                'previous': previous_page,
                'count': count,
                'results': result,
                'page_size': page_size,
            },
            status=status_code,
        )

    @staticmethod
    def not_found(data=None, status_code=status.HTTP_404_NOT_FOUND) -> Response:
        if not data:
            data = ResponseFormat.failure_data_format(
                msg=trans('Not found'),
                status_code=404,
            )
        return Response(data, status=status_code)

    @staticmethod
    def forbidden(data=None, status_code=status.HTTP_403_FORBIDDEN) -> Response:
        if not data:
            data = ResponseFormat.failure_data_format(
                msg=trans('Forbidden'),
                status_code=404,
            )
        return Response(data, status=status_code)

    @staticmethod
    def not_authorized(data=None, status_code=status.HTTP_401_UNAUTHORIZED) -> Response:
        if not data:
            data = ResponseFormat.failure_data_format(
                msg=trans('Not authorized'),
                status_code=401,
            )
        return Response(data, status=status_code)

    @staticmethod
    def list(data, status_code=status.HTTP_200_OK) -> Response:
        return Response(
            data={
                'results': data,
            },
            status=status_code
        )

    @staticmethod
    def created(data, status_code=status.HTTP_201_CREATED) -> Response:
        return Response(
            data={
                'results': data,
            },
            status=status_code
        )

    @staticmethod
    def retrieved(data, status_code=status.HTTP_200_OK) -> Response:
        return Response(
            data={
                'results': data,
            },
            status=status_code
        )

    @staticmethod
    def updated(data=None, status_code=status.HTTP_200_OK) -> Response:
        if not data:
            data = {}
        return Response(
            data={
                'results': data
            } if data else {},
            status=status_code
        )

    @staticmethod
    def deleted(data=None, status_code=status.HTTP_204_NO_CONTENT) -> Response:
        if not data:
            data = {}
        return Response(
            data=data,
            status=status_code
        )

    @staticmethod
    def response_format(status_code = None, msg = "", data = None)->Response:
        if not data:
            data = {}
        body = {
            "status_code": status_code,
            "msg": msg,
            "data": data
        }
        return Response(
            data=body,
            status=200
        )
