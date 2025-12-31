
from ..models.products import Attribute, AttributeValue, M2MAttribute
from ...shared.response import ResponseBuilder, ResponseCodes
from ...shared.decorator.decorator import validate_exception
from ..serializers.m2m_attribute import M2MAtrributeCreateSerializer, M2MAtrributeDetailSerializer
from ...shared.mixins import CreateMixin, DestroyMixin, ListMixin, UpdateMixin
from django.db import transaction
class M2MAttributeUpdateAPI(CreateMixin):
    @validate_exception()
    def post(self, request, *args, **kwargs):
        attribute = request.data.get('attribute')
        attribute_value = request.data.get('attribute_value', [])
        print("attribute_value_check_request",attribute_value)
        if not attribute:
            return ResponseBuilder.build(
                code=ResponseCodes.INVALID_INPUT
            )
        try:
            try:
                Attribute.objects.get(pk=attribute)
            except Attribute.DoesNotExist:
                return ResponseBuilder.build(code=ResponseCodes.INVALID_INPUT)
            with transaction.atomic():
                db_value_ids = set(
                    M2MAttribute.objects.filter(attribute_id=attribute)
                    .values_list('attribute_value_id', flat=True)
                )
                print("db_value_ids",db_value_ids)
                try:
                    request_value_ids = set(int(v) for v in attribute_value)
                except:
                    return ResponseBuilder.build(code=ResponseCodes.INVALID_INPUT)
                print("request_value_ids",request_value_ids)
                M2MAttribute.objects.filter(
                    attribute_id=attribute,
                    attribute_value_id__in=db_value_ids - request_value_ids
                ).update(is_deleted=True)
                for value_id in request_value_ids - db_value_ids:
                    if not AttributeValue.objects.filter(pk=value_id).exists():
                        raise AttributeValue.DoesNotExist
                    M2MAttribute.objects.create(
                        attribute_id=attribute,
                        attribute_value_id=value_id
                    )
            return ResponseBuilder.build(
                code=ResponseCodes.SUCCESS
            )
        except Exception as e:
            return ResponseBuilder.build(
                code=ResponseCodes.INVALID_INPUT,
                errors=str(e)
            )