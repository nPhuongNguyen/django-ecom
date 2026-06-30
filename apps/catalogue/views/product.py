from django.shortcuts import render
from django.views import View

from apps.catalogue.models.products import Product
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
        return render(request,'product/list.html', context=context)
    
class ProductDetailView(View):
    MASK_VIEW_CONFIG_UPDATE = {
        **MASK_VIEW_CONFIG,
        "space_code": "product-list"
    }
    @mask_view(**MASK_VIEW_CONFIG_UPDATE)
    def get(self, request, *args, context, **kwargs):
        pk = kwargs.get('pk')
        if not pk:
            return render(request,'admin/notfound/notfound.html', context=context)
        context['pk'] = pk
        return render(request, 'product/detail.html', context=context)
    
class ProductCreateView(View):
    MASK_VIEW_CONFIG_UPDATE = {
        **MASK_VIEW_CONFIG,
        "space_code": "product-create"
    }
    @mask_view(**MASK_VIEW_CONFIG_UPDATE)
    def get(self, request, *args, context, **kwargs):
        return render(request, 'product/create.html', context=context)