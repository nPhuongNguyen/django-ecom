from rest_framework.views import APIView

from apps.accounts.pydantic.user import UserInfoPydantic
from apps.sales.serializers.cart import AddToCartSerializer, CartDeleteItemSerializer, CartUpdateItemSerializer
from apps.shared.decorator.decorator import token_required, validate_exception
from apps.shared.response import ResponseBuilder, ResponseCodes
from apps.sales.services.cart import cart_service
from apps.logging import logging_log as lg
from pydantic import ValidationError as PydanticValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError

from apps.shared.utils.contextvar import RequestContext

class CartCreateAPI(APIView):
    @validate_exception()
    @token_required()
    def post(self, request, *args, **kwargs):
        try:
            function_name = "CartCreateAPI"
            RequestContext.set_request_func(function_name)
            data_cart = request.data_input
            data_cart_body = data_cart.get("body", {})
            data_safe_cart = AddToCartSerializer(data=data_cart_body)
            data_safe_cart.is_valid(raise_exception=True)
            data_safe_cart = data_safe_cart.validated_data
            data_user = request.user
            data_safe_user = UserInfoPydantic(**data_user)
            cart_service.add_to_cart(data_safe_user.email, data_safe_cart)   
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
    @token_required()
    def get(self, request, *args, **kwargs):
        try:
            function_name = "CartDetailAPI"
            RequestContext.set_request_func(function_name)
            data_user = request.user
            data_safe_user = UserInfoPydantic(**data_user)
            cart_data = cart_service.get_cart(data_safe_user.email)
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
            data=cart_data.model_dump()
        )
        
class CartUpdateAPI(APIView):
    @validate_exception()
    @token_required()
    def post(self, request, *args, **kwargs):
        try:
            function_name = "CartUpdateAPI"
            RequestContext.set_request_func(function_name)
            data_cart = request.data_input
            data_cart_body = data_cart.get("body", {})
            data_safe_cart = CartUpdateItemSerializer(data=data_cart_body)
            data_safe_cart.is_valid(raise_exception=True)
            data_user = request.user
            data_safe_user = UserInfoPydantic(**data_user)
            user_id_update_cart = cart_service.update_cart(data_safe_user.email, data_safe_cart.validated_data)
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
        
class CartDeleteAPI(APIView):
    @validate_exception()
    @token_required()
    def post(self, request, *args, **kwargs):
        try:
            function_name = "CartDeleteAPI"
            RequestContext.set_request_func(function_name)
            data_cart = request.data_input
            data_cart_body = data_cart.get("body", {})
            data_safe_cart = CartDeleteItemSerializer(data=data_cart_body)
            data_safe_cart.is_valid(raise_exception=True)
            data_user = request.user
            data_safe_user = UserInfoPydantic(**data_user)
            user_id_update_cart = cart_service.delete_from_cart(data_safe_user.email, data_safe_cart.validated_data["product_variant_id"])
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