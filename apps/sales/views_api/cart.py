from rest_framework.views import APIView

from apps.sales.serializers.cart_item import CartItemSerializer, CartUpdateItemSerializer
from apps.shared.decorator.decorator import validate_exception
from apps.shared.response import ResponseBuilder, ResponseCodes
from apps.sales.services.cart import cart_service
from apps.logging import logging_log as lg
from pydantic import ValidationError as PydanticValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError

from apps.shared.utils.contextvar import RequestContext

class CartCreateAPI(APIView):
    
    @validate_exception()
    def post(self, request, *args, **kwargs):
        try:
            function_name = "CartCreateAPI"
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
        except (PydanticValidationError, DRFValidationError) as e:
            errors = (
                e.errors()
                if isinstance(e, PydanticValidationError)
                else e.detail
            )
            lg.log_error(
                message="[VALIDATION_ERROR] Invalid cart data",
                errors=errors
            )
            return ResponseBuilder.build(
                ResponseCodes.INVALID_INPUT
            )
        return ResponseBuilder.build(
            ResponseCodes.SUCCESS
        )
        
class CartDetailAPI(APIView):
    @validate_exception()
    def get(self, request, *args, **kwargs):
        try:
            function_name = "CartDetailAPI"
            RequestContext.set_request_func(function_name)
            user_id_input = kwargs.get("user_id")
            if not user_id_input:
                lg.log_error(
                    message="[VALIDATION_ERROR] user_id is required in URL"
                )
                return ResponseBuilder.build(
                    ResponseCodes.INVALID_INPUT
                )
            get_cart = cart_service.get_cart(user_id_input)
            if not get_cart:
                lg.log_error(
                    message="[GET_CART_ERROR] Failed to get cart for user_id",
                    user_id=user_id_input
                )
                return ResponseBuilder.build(
                    ResponseCodes.SYSTEM_ERROR
                )
        except (PydanticValidationError, DRFValidationError) as e:
            errors = (
                e.errors()
                if isinstance(e, PydanticValidationError)
                else e.detail
            )
            lg.log_error(
                message="[VALIDATION_ERROR] Invalid user_id",
                errors=errors
            )
            return ResponseBuilder.build(
                ResponseCodes.INVALID_INPUT
            )
        return ResponseBuilder.build(
            ResponseCodes.SUCCESS,
            data=get_cart.model_dump()
        )
        
class CartUpdateAPI(APIView):
    @validate_exception()
    def put(self, request, *args, **kwargs):
        try:
            function_name = "CartUpdateAPI"
            RequestContext.set_request_func(function_name)
            user_id_input = kwargs.get("user_id")
            if not user_id_input:
                lg.log_error(
                    message="[VALIDATION_ERROR] user_id is required in URL"
                )
                return ResponseBuilder.build(
                    ResponseCodes.INVALID_INPUT
                )
            data_cart = request.data_input
            data_cart_body = data_cart.get("body", {})
            data_safe_cart = CartUpdateItemSerializer(data=data_cart_body)
            data_safe_cart.is_valid(raise_exception=True)
            user_id_update_cart = cart_service.update_cart(user_id_input, data_safe_cart.validated_data)
        except (PydanticValidationError, DRFValidationError) as e:
            errors = (
                e.errors()
                if isinstance(e, PydanticValidationError)
                else e.detail
            )
            lg.log_error(
                message="[VALIDATION_ERROR] Invalid user_id",
                errors=errors
            )
            return ResponseBuilder.build(
                ResponseCodes.INVALID_INPUT
            )
        return ResponseBuilder.build(
            ResponseCodes.SUCCESS,
            data = user_id_update_cart
        )