from apps.catalogue.models.products import Product
from apps.catalogue.serializers.products import ProductCreateSerializer, ProductDetailSerializer, ProductListSerializer, ProductUpdateSerializer
from apps.shared.decorator.decorator import token_required, validate_exception
from apps.shared.mixins import CreateMixin, DestroyMixin, DetailMixin, ListMixin, UpdateMixin
class ProductListAPI(ListMixin, CreateMixin, DestroyMixin):
    queryset = Product.objects.all()
    serializer_class_list = ProductListSerializer
    search_fields = ['name']
    ordering_fields = ['name']
    filterset_fields = ['is_active']
    @validate_exception()
    @token_required()
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
class ProductCreateAPI(CreateMixin):
    serializer_class_create = ProductCreateSerializer
    serializer_class_detail = ProductDetailSerializer
    @validate_exception()
    @token_required()
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
class ProductUpdateAPI(UpdateMixin):
    queryset = Product.objects.all()
    serializer_class_update = ProductUpdateSerializer
    serializer_class_detail = ProductDetailSerializer
    @validate_exception()
    @token_required()
    def post(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

class ProductDestroyAPI(DestroyMixin):
    queryset = Product.objects.all()
    @validate_exception()
    @token_required()
    def post(self, request, *args, **kwargs):
        return self.destroy_many(request, *args, **kwargs) 
    

class ProductChangeStatusAPI(UpdateMixin):
    queryset = Product.objects.all()
    serializer_class_update = ProductUpdateSerializer
    serializer_class_detail = ProductDetailSerializer
    @validate_exception()
    @token_required()
    def post(self, request, *args, **kwargs):
        return self.change_status(request, *args, **kwargs)
    

class ProductDetailAPI(DetailMixin):
    queryset = Product.objects.select_related('category').prefetch_related('variants').all()
    serializer_class_detail = ProductDetailSerializer
    @token_required()
    @validate_exception()
    def get(self, request, *args, **kwargs):
        return self.detail(request, *args, **kwargs)
