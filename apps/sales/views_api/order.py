
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from apps.sales.pydantic.order import OrderPydantic
from apps.sales.serializers.order import OrderCreateInputSerializer
from apps.shared.decorator.decorator import validate_exception
from apps.shared.response import ResponseBuilder, ResponseCodes
from apps.shared.utils.contextvar import RequestContext
from apps.logging import logging_log as lg
from apps.sales.services.order import oreder_service

class OrderAPI(APIView):
    @validate_exception()
    def post(self, request, *args, **kwargs):
        try:
            function_name = "OrderAPI"
            RequestContext.set_request_func(function_name)
            data_order = request.data_input
            data_order_body = data_order.get("body", {})
            data_input = OrderCreateInputSerializer(data=data_order_body)
            data_input.is_valid(raise_exception=True)
            data_input_safe = data_input.validated_data
            oreder_service.create_order(data_input_safe)
        except ValidationError as e:
            lg.log_error(
                message="[VALIDATION_ERROR] Invalid order data",
                errors=e.detail
            )
            return ResponseBuilder.build(
                ResponseCodes.INVALID_INPUT
            )
        return ResponseBuilder.build(
            ResponseCodes.SUCCESS
        )