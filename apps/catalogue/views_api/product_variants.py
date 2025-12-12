from apps.catalogue.models.products import ProductVariant
from apps.catalogue.serializers.product_variants import ProductVariantCreateSerializer, ProductVariantDetailSerializer, ProductVariantListSerializer, ProductVariantUpdateSerializer
from ...shared.decorator.decorator import validate_exception
from apps.shared.mixins import CreateMixin, DestroyMixin, ListMixin, UpdateMixin
class ProductVariantListAPI(ListMixin):
    queryset = ProductVariant.objects.all()
    serializer_class_list = ProductVariantListSerializer
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
class ProductVariantCreateAPI(CreateMixin):
    queryset = ProductVariant.objects.all()
    serializer_class_create = ProductVariantCreateSerializer
    serializer_class_detail = ProductVariantDetailSerializer
    @validate_exception()
    def post(self, request, *args, **kwargs):
        return self.create(request, args, kwargs)
    
class ProductVariantDestroyAPI(DestroyMixin):
    queryset = ProductVariant.objects.all()
    @validate_exception()
    def post(self, request, *args, **kwargs):
        return self.destroy_many(request, *args, **kwargs) 
    
class ProductVariantChangeStatusAPI(UpdateMixin):
    queryset = ProductVariant.objects.all()
    serializer_class_update = ProductVariantUpdateSerializer
    serializer_class_detail = ProductVariantDetailSerializer
    @validate_exception()
    def post(self, request, *args, **kwargs):
        return self.change_status(request, *args, **kwargs)
    
class ProductVariantUpdateAPI(UpdateMixin):
    queryset = ProductVariant.objects.all()
    serializer_class_update = ProductVariantUpdateSerializer
    serializer_class_detail = ProductVariantDetailSerializer
    @validate_exception()
    def post(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    