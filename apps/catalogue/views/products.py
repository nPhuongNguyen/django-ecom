from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.views import View

from apps.catalogue.models.products import Product
from apps.shared.decorator.views import mask_view

MASK_VIEW_CONFIG ={
    "accordion": "products",
    "space_code": "product-list"
}

class ProductListView(View):
    @mask_view(**MASK_VIEW_CONFIG)
    def get(self, request, *args, context, **kwargs):
        return render(request,'products/list.html', context=context)
    
class ProductDetailView(View):
    @mask_view(**MASK_VIEW_CONFIG)
    def get(self, request, slug, *args, context, **kwargs):
        if slug:
            product_info = (Product.objects.select_related('category')
                .prefetch_related('variants').get(slug=slug)
            )
            if product_info.category:
                print(product_info.category.name)
            for variant in product_info.variants.all():
                print(variant.name, variant.price, variant.sku)
        return render(request, 'products/detail.html', context=context)
    
class ProductCreateView(View):
    @mask_view(**MASK_VIEW_CONFIG)
    def get(self, request, *args, context, **kwargs):
        return render(request, 'products/create.html', context=context)