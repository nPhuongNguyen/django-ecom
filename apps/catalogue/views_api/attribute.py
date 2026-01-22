

from ...shared.decorator.decorator import validate_exception
from ..serializers.attribute import AttributeCreateSerializer, AttributeDetailSerializer, AttributeListSerializer, AttributeUpdateSerializer
from ..models.products import Attribute
from ...shared.mixins import CreateMixin, DestroyMixin, ListMixin, UpdateMixin


class AttributeListAPI(ListMixin):
    queryset = Attribute.objects.all()
    serializer_class_list = AttributeListSerializer
    search_fields = ['name']
    filterset_fields =['is_active']
    ordering_fields = ['name']
    def get(self, request, *arg, **kwargs):
        return self.list(request, *arg, **kwargs)
    
class AttributeCreateAPI(CreateMixin):
    serializer_class_create = AttributeCreateSerializer
    serializer_class_detail = AttributeDetailSerializer
    @validate_exception()
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
class AttributeUpdateAPI(UpdateMixin):
    queryset = Attribute.objects.all()
    serializer_class_update = AttributeUpdateSerializer
    serializer_class_detail = AttributeDetailSerializer
    @validate_exception()
    def post(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
class AttributeDestroyAPI(DestroyMixin):
    queryset = Attribute.objects.all()
    @validate_exception()
    def post(self, request, *args, **kwargs):
        return self.destroy_many(request, *args, **kwargs) 
    
class AttributeChangeStatusAPI(UpdateMixin):
    queryset = Attribute.objects.all()
    serializer_class_update = AttributeUpdateSerializer
    serializer_class_detail = AttributeDetailSerializer
    @validate_exception()
    def post(self, request, *args, **kwargs):
        return self.change_status(request, *args, **kwargs)