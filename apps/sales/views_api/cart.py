from rest_framework.views import APIView

from apps.sales.serializers.cart_item import CartItemSerializer
from apps.shared.decorator.decorator import validate_exception
from apps.shared.response import ResponseBuilder, ResponseCodes
from apps.sales.services.cart import cart_service
from apps.logging import logging_log as lg
from rest_framework.exceptions import ValidationError

from apps.shared.utils.contextvar import RequestContext

class CartAPI(APIView):
    @validate_exception()
    def post(self, request, *args, **kwargs):
        try:
            function_name = "CartAPI"
            RequestContext.set_request_func(function_name)
            data_cart = request.data_input
            data_cart_body = data_cart.get("body", {})
            data_safe_cart = CartItemSerializer(data=data_cart_body)
            data_safe_cart.is_valid(raise_exception=True)
            data_safe_cart = data_safe_cart.validated_data
            add_to_cart = cart_service.add_to_cart(data_safe_cart)
            if not add_to_cart:
                lg.log_error(
                    message="[ADD_TO_CART_ERROR] Failed to add item to cart",
                    data=data_cart
                )
                return ResponseBuilder.build(
                    ResponseCodes.SYSTEM_ERROR
                )
        except ValidationError as e:
            lg.log_error(
                message="[VALIDATION_ERROR] Invalid cart data",
                errors=e.detail
            )
            return ResponseBuilder.build(
                ResponseCodes.INVALID_INPUT
            )
        return ResponseBuilder.build(
            ResponseCodes.SUCCESS
        )