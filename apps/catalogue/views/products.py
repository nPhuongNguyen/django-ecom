from django.shortcuts import render
from django.views import View

from apps.catalogue.models.products import Product
from apps.shared.decorator.views import mask_view

MASK_VIEW_CONFIG ={
    "accordion": "product",
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
            product = Product.objects.select_related('category').get(slug=slug)
            context['obj_product'] = product
        except Product.DoesNotExist:
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