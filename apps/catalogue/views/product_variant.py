from django.shortcuts import render
from django.views import View

from ..models.products import ProductVariant

from ...shared.decorator.views import mask_view

MASK_VIEW_CONFIG ={
    "accordion": "ecommerce",
    "accordion_child": "product-variant"
}

class ProductVariantListView(View):
    MASK_VIEW_CONFIG_UPDATE = {
        **MASK_VIEW_CONFIG,
        "space_code": "product-variant-list"
    }
    @mask_view(**MASK_VIEW_CONFIG_UPDATE)
    def get(self, request, *args, context, **kwargs):
        return render(request,'product_variants/list.html', context=context)
    
class ProductVariantDetailView(View):
    MASK_VIEW_CONFIG_UPDATE = {
        **MASK_VIEW_CONFIG,
        "space_code": "product-variant-list"
    }
    @mask_view(**MASK_VIEW_CONFIG_UPDATE)
    def get(self, request, *args, context, **kwargs):
        if 'pk' in kwargs:
            obj_product_variant = ProductVariant.objects.get(pk=kwargs.get('pk'), is_deleted = False)
            context['obj_product_variant'] = obj_product_variant
        else:
            return render(request,'admin/notfound/notfound.html', context=context)
        return render(request,'product_variants/detail.html', context=context)
    
class ProductVariantCreateView(View):
    MASK_VIEW_CONFIG_UPDATE = {
        **MASK_VIEW_CONFIG,
        "space_code": "product-variant-create"
    }
    @mask_view(**MASK_VIEW_CONFIG_UPDATE)
    def get(self, request, *args, context, **kwargs):
        return render(request,'product_variants/create.html', context=context)