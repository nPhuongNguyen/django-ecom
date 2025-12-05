from django.shortcuts import render
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
    def get(self, request, *args, context, **kwargs):
        slug = kwargs.get('slug')
        try:
            product = Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            return render(request,'admin/notfound/notfound.html', context=context)
        return render(request, 'products/detail.html', context=context)
    
class ProductCreateView(View):
    @mask_view(**MASK_VIEW_CONFIG)
    def get(self, request, *args, context, **kwargs):
        return render(request, 'products/create.html', context=context)