
from ..models.products import Attribute, AttributeValue, M2MAttribute
from ...shared.response import ResponseBuilder, ResponseCodes
from ...shared.decorator.decorator import validate_exception
from ..serializers.m2m_attribute import M2MAtrributeCreateSerializer, M2MAtrributeDetailSerializer
from ...shared.mixins import CreateMixin, DestroyMixin, ListMixin, UpdateMixin
from django.db import transaction
class M2MAttributeCreateAPI(CreateMixin):
    @validate_exception()
    def post(self, request, *args, **kwargs):
        attribute = request.data.get('attribute')
        attribute_value = request.data.get('attribute_value')
        if not attribute or len(attribute_value) == 0:
            return ResponseBuilder.build(
                code=ResponseCodes.INVALID_INPUT
            )
        try:
            try:
                Attribute.objects.get(pk=attribute)
            except Attribute.DoesNotExist:
                return ResponseBuilder.build(code=ResponseCodes.INVALID_INPUT)
            with transaction.atomic():
                for i in attribute_value:
                    if not AttributeValue.objects.filter(pk=i).exists():
                        raise AttributeValue.DoesNotExist
                    
                    M2MAttribute.objects.create(
                        attribute_id = attribute,
                        attribute_value_id = i
                    )
            return ResponseBuilder.build(
                code=ResponseCodes.SUCCESS
            )
        except Exception as e:
            return ResponseBuilder.build(
                code=ResponseCodes.INVALID_INPUT,
                errors=str(e)
            )