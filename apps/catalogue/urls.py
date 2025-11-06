from django.urls import path

from apps.catalogue import views

#Product
urlpatterns =[
    path('product-list', views.ProductListView.as_view(), name='ProductListView')
]