from apps.catalogue.models.products import Product
from apps.catalogue.serializers.products import ProductCreateSerializer, ProductDetailSerializer, ProductListSerializer, ProductUpdateSerializer
from apps.shared.decorator.decorator import token_required, validate_exception
from apps.shared.mixins import CreateMixin, DestroyMixin, ListMixin, UpdateMixin
class ProductListAPI(ListMixin, CreateMixin, DestroyMixin):
    queryset = Product.objects.all()
    serializer_class_list = ProductListSerializer
    search_fields = ['name']
    ordering_fields = ['name']
    # @token_required()
    @validate_exception()
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
class ProductCreateAPI(CreateMixin):
    serializer_class_create = ProductCreateSerializer
    serializer_class_detail = ProductDetailSerializer
    @validate_exception()
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
    

class ProductChangeStatusAPI(UpdateMixin):
    queryset = Product.objects.all()
    serializer_class_update = ProductUpdateSerializer
    serializer_class_detail = ProductDetailSerializer
    @validate_exception()
    def post(self, request, *args, **kwargs):
        return self.change_status(request, *args, **kwargs)
    

class ProductDetailAPI(UpdateMixin, DestroyMixin):
    queryset = Product.objects.all()
    serializer_class_detail = ProductDetailSerializer
    serializer_class_update = ProductUpdateSerializer
    @validate_exception()
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
