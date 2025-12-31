from django.shortcuts import render
from django.views import View

from ..models.products import Attribute, M2MAttribute

from ...shared.decorator.views import mask_view

MASK_VIEW_CONFIG ={
    "accordion": "ecommerce",
    "accordion_child": "attribute"
}

class AttributeListView(View):
    MASK_VIEW_CONFIG_UPDATE = {
        **MASK_VIEW_CONFIG,
        "space_code": "attribute-list"
    }
    @mask_view(**MASK_VIEW_CONFIG_UPDATE)
    def get(self, request, *args, context, **kwargs):
        return render(request,'attributes/list.html', context=context)
    
class AttributeDetailView(View):
    MASK_VIEW_CONFIG_UPDATE = {
        **MASK_VIEW_CONFIG,
        "space_code": "attribute-list"
    }
    @mask_view(**MASK_VIEW_CONFIG_UPDATE)
    def get(self, request, *args, context, **kwargs):
        pk = kwargs.get('pk')
        try:
            attribute = Attribute.objects.get(pk=pk)
            attribute_value = M2MAttribute.objects.filter(attribute_id = attribute)
            context['obj_attribute'] = attribute
            context['obj_attribute_value'] = attribute_value
        except:
            return render(request,'admin/notfound/notfound.html', context=context)
        return render(request,'attributes/detail.html', context=context)
    
class AttributeCreateView(View):
    MASK_VIEW_CONFIG_UPDATE = {
        **MASK_VIEW_CONFIG,
        "space_code": "attribute-create"
    }
    @mask_view(**MASK_VIEW_CONFIG_UPDATE)
    def get(self, request, *args, context, **kwargs):
        return render(request,'attributes/create.html', context=context)