from apps.catalogue.models.products import ProductVariant
from apps.catalogue.serializers.product_variants import ProductVariantCreateSerializer, ProductVariantDetailSerializer, ProductVariantListSerializer, ProductVariantUpdateSerializer
from apps.shared.mixins import CreateMixin, DestroyMixin, ListMixin, UpdateMixin
class ProductVariantListAPI(ListMixin, CreateMixin, DestroyMixin):
    queryset = ProductVariant.objects.all()
    serializer_class_create = ProductVariantCreateSerializer
    serializer_class_list = ProductVariantListSerializer
    serializer_class_detail = ProductVariantDetailSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy_many(request, *args, **kwargs)
    
class ProductVariantDetailAPI(UpdateMixin, DestroyMixin):
    queryset = ProductVariant.objects.all()
    serializer_class_update = ProductVariantUpdateSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
