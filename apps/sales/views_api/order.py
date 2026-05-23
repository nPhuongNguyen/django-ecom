
from rest_framework.views import APIView
from django.db import transaction
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
        function_name = "OrderAPI"
        RequestContext.set_request_func(function_name)
        data_order = request.data_input
        data_order_body = data_order.get("body", {})
        data_input = OrderCreateInputSerializer(data=data_order_body)
        if not data_input.is_valid():
            lg.log_error(
                message="[VALIDATION_ERROR] Invalid order body",
                data=data_order,
                errors=data_input.errors
            )
            return ResponseBuilder.build(
                ResponseCodes.INVALID_INPUT
            )
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
        create_order = oreder_service.create_order(data_safe_order, data_safe_order_item)
            
        return ResponseBuilder.build(
            ResponseCodes.SUCCESS
        )