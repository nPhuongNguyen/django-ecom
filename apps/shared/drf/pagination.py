__all__ = [
    'StandardResultsSetPagination',
]

from rest_framework.pagination import PageNumberPagination

from apps.shared.response import ResponseFormat


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'pageSize'
    max_page_size = 1000
    page_size_query_description = (
        "page_size_query_description (value -1 with get not page, maximum: 1000).",
    )

    def get_page_size(self, request):
        page_size_int = self.page_size
        page_size_str = request.query_params.get(self.page_size_query_param, str(page_size_int))
        try:
            page_size_int = int(page_size_str)
        except (KeyError, ValueError):
            pass
        if page_size_int == -1:
            page_size_str = 1000
        return self.positive_int(page_size_str, strict=True, cutoff=self.max_page_size)

    def get_paginated_response(self, data):
        return ResponseFormat.pagination(
            result=data,
            count=self.page.paginator.count,
            page_size=self.page.paginator.per_page,
            next_page=self.page.next_page_number() if self.page.has_next() else 0,
            previous_page=self.page.previous_page_number() if self.page.has_previous() else 0,
        )

    @staticmethod
    def positive_int(integer_string, strict=False, cutoff=None):
        """
        Cast a string to a strictly positive integer.
        """
        ret = int(integer_string)
        if ret < 0 or (ret == 0 and strict):
            raise ValueError()
        if cutoff:
            return min(ret, cutoff)
        return ret
