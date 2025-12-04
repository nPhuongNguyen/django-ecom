from apps.catalogue.models.products import Product
from apps.catalogue.serializers.products import ProductCreateSerializer, ProductDetailSerializer, ProductListSerializer, ProductUpdateSerializer
from apps.shared.mixins import CreateMixin, DestroyMixin, ListMixin, UpdateMixin
class ProductListAPI(ListMixin, CreateMixin, DestroyMixin):
    queryset = Product.objects.all()
    serializer_class_list = ProductListSerializer
    search_fields = ['name']
    ordering_fields = ['name']
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
class ProductCreateAPI(CreateMixin):
    serializer_class_create = ProductCreateSerializer
    serializer_class_detail = ProductDetailSerializer
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
class ProductUpdateAPI(UpdateMixin):
    queryset = Product.objects.all()
    serializer_class_update = ProductUpdateSerializer
    serializer_class_detail = ProductDetailSerializer
    def post(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

class ProductDestroyAPI(DestroyMixin):
    queryset = Product.objects.all()
    def post(self, request, *args, **kwargs):
        return self.destroy_many(request, *args, **kwargs) 
class ProductDetailAPI(UpdateMixin, DestroyMixin):
    queryset = Product.objects.all()
    serializer_class_detail = ProductDetailSerializer
    serializer_class_update = ProductUpdateSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
