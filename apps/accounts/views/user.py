
from django.shortcuts import render
from django.views import View
from ...shared.decorator.views import mask_view


MASK_VIEW_CONFIG ={
    "accordion": "account",
    "accordion_child": "user"
}

class UserListView(View):
    MASK_VIEW_CONFIG_UPDATE = {
        **MASK_VIEW_CONFIG,
        "space_code": "user-list"
    }
    @mask_view(**MASK_VIEW_CONFIG_UPDATE)
    def get(self, request, *args, context, **kwargs):
        return render(request,'user/list.html', context=context)
