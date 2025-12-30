from django.shortcuts import render
from django.views import View

from apps.catalogue.models.products import Product
from ..serializers.products import ProductDetailSerializer
from apps.shared.decorator.views import mask_view

MASK_VIEW_CONFIG ={
    "accordion": "ecommerce",
    "accordion_child": "product",
    "menu_item_show": "product"
}

class ProductListView(View):
    MASK_VIEW_CONFIG_UPDATE = {
        **MASK_VIEW_CONFIG,
        "space_code": "product-list"
    }
    @mask_view(**MASK_VIEW_CONFIG_UPDATE)
    def get(self, request, *args, context, **kwargs):
        return render(request,'products/list.html', context=context)
    
class ProductDetailView(View):
    MASK_VIEW_CONFIG_UPDATE = {
        **MASK_VIEW_CONFIG,
        "space_code": "product-list"
    }
    @mask_view(**MASK_VIEW_CONFIG_UPDATE)
    def get(self, request, *args, context, **kwargs):
        slug = kwargs.get('slug')
        try:
            product = Product.objects.get(slug=slug, is_deleted = False)
            context['obj_product'] = product
            info_product = ProductDetailSerializer(instance = product).data
            print('obj_product',info_product)
        except:
            return render(request,'admin/notfound/notfound.html', context=context)
        return render(request, 'products/detail.html', context=context)
    
class ProductCreateView(View):
    MASK_VIEW_CONFIG_UPDATE = {
        **MASK_VIEW_CONFIG,
        "space_code": "product-create"
    }
    @mask_view(**MASK_VIEW_CONFIG_UPDATE)
    def get(self, request, *args, context, **kwargs):
        return render(request, 'products/create.html', context=context)