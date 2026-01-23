from ..models.products import AttributeValue
from ...shared.decorator.decorator import token_required, validate_exception
from ..serializers.attribute_value import AttributeValueCreateSerializer, AttributeValueDetailSerializer, AttributeValueListSerializer
from ...shared.mixins import CreateMixin, DestroyMixin, ListMixin, UpdateMixin
from django.db import transaction
from ..models.products import M2MAttribute

class AttributeValueCreateAPI(CreateMixin):
    serializer_class_create = AttributeValueCreateSerializer
    serializer_class_detail = AttributeValueDetailSerializer

    def perform_create(self, serializer, **kwargs):
        input_data = self.get_create_data()
        result = super().perform_create(serializer, **kwargs)
        attribute = input_data.get('attribute')
        if attribute:
            M2MAttribute.objects.create(
                attribute_id=attribute,
                attribute_value_id=result.id   
            )
        return result
        
    @validate_exception()
    @token_required()
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
class AttributeValueListAPI(ListMixin):
    queryset = AttributeValue.objects.all()
    serializer_class_list = AttributeValueListSerializer
    search_fields = ['name']
    filterset_fields =['is_active']
    ordering_fields = ['name']
    @validate_exception()
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)