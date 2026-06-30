from apps.catalogue.serializers.product_attribute import ProductAttributeCreateSerializer, ProductAttributeDetailSerializer, ProductAttributeInputSerializer
from apps.shared.decorator.decorator import validate_exception
from apps.shared.mixins import CreateMixin, DestroyMixin, ListMixin, UpdateMixin, DetailMixin
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from apps.shared.response import ResponseBuilder, ResponseCodes
from apps.shared.utils.contextvar import RequestContext
from apps.logging import logging_log as lg
class ProductAttributeCreateAPI(CreateMixin):
    @validate_exception()
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)