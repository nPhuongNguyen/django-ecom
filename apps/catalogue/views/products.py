from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.views import View
class ProductListView(View):
    def get(self, request, *args, **kwargs):
        products = [
            {"id": 1, "name": "Son môi", "price": "200,000đ", "status": "Còn hàng"},
            {"id": 2, "name": "Kem dưỡng", "price": "350,000đ", "status": "Hết hàng"},
            {"id": 3, "name": "Nước hoa", "price": "1,200,000đ", "status": "Còn hàng"},
        ]
        return render(request,'products/list.html',{"products": products})
