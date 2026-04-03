
from ..models.products import Attribute, AttributeValue, M2MAttribute
from ...shared.response import ResponseBuilder, ResponseCodes
from ...shared.decorator.decorator import validate_exception
from ..serializers.m2m_attribute import M2MAtrributeCreateSerializer, M2MAtrributeDetailSerializer, M2MAtrributeInputSerializer
from ...shared.mixins import CreateMixin, DestroyMixin, ListMixin, UpdateMixin
from django.db import transaction
from apps.logging import logging_log as lg
class M2MAttributeUpdateAPI(CreateMixin):
    serializer_class_create = M2MAtrributeCreateSerializer
    serializer_class_detail = M2MAtrributeDetailSerializer

    def create(self, request, *args, **kwargs):
        dataa_input = request.data_input
        serializer = M2MAtrributeInputSerializer(data=dataa_input)
        if not serializer.is_valid():
            return ResponseBuilder.build(
                code=ResponseCodes.INVALID_INPUT,
                errors=serializer.errors
            )
        data_safe = serializer.validated_data
        data_body_input = data_safe.get("body", {})
        attribute_id = data_body_input.get('attribute')
        list_attribute_value = set(data_body_input.get('list_attribute_value', []))

        # Lấy danh sách hiện tại trong DB
        existing_values = set(
            M2MAttribute.objects.filter(
                attribute_id=attribute_id
            ).values_list('attribute_value_id', flat=True)
        )

        #DELETE
        to_delete = existing_values - list_attribute_value
        if to_delete:
            M2MAttribute.objects.filter(
                attribute_id=attribute_id,
                attribute_value_id__in=to_delete
            ).delete()


        #ADD
        to_create = list_attribute_value - existing_values
        for obj_id in to_create:
            M2MAttribute.objects.create(
                attribute_id=attribute_id,
                attribute_value_id=obj_id
            )

        
        return ResponseBuilder.build(
            code=ResponseCodes.SUCCESS
        )

    @validate_exception()
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)