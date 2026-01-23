from ..models.products import AttributeValue
from ...shared.decorator.decorator import validate_exception
from ..serializers.attribute_value import AttributeValueCreateSerializer, AttributeValueDetailSerializer, AttributeValueListSerializer
from ...shared.mixins import CreateMixin, DestroyMixin, ListMixin, UpdateMixin
class AttributeValueCreateAPI(CreateMixin):
    serializer_class_create = AttributeValueCreateSerializer
    serializer_class_detail = AttributeValueDetailSerializer
    @validate_exception()
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