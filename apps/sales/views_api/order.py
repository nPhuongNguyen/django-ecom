
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
            data_input_safe = OrderPydantic(**data_input_safe)
            data_safe_order = {
                "user_id": data_input_safe.user_id,
                "note": data_input_safe.note,
                "total_amount": data_input_safe.total_amount,
                "subtotal_amount": data_input_safe.subtotal_amount,
                "discount_amount": data_input_safe.discount_amount,
            }
            data_safe_order_item = data_input_safe.items
            oreder_service.create_order(data_safe_order, data_safe_order_item)
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