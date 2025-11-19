from apps.catalogue.models.products import Product
from apps.catalogue.serializers.products import ProductCreateSerializer, ProductDetailSerializer, ProductListSerializer, ProductUpdateSerializer
from apps.shared.mixins import CreateMixin, DestroyMixin, ListMixin, UpdateMixin
class ProductListAPI(ListMixin, CreateMixin, DestroyMixin):
    queryset = Product.objects.all()
    serializer_class_list = ProductListSerializer
    serializer_class_create = ProductCreateSerializer
    serializer_class_detail = ProductDetailSerializer
    search_fields = ['name']
    ordering_fields = ['name']

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy_many(request, *args, **kwargs)
    
class ProductDetailAPI(UpdateMixin, DestroyMixin):
    queryset = Product.objects.all()
    serializer_class_detail = ProductDetailSerializer
    serializer_class_update = ProductUpdateSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
