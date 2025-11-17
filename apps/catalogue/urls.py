from django.urls import path

from apps.catalogue import views

#Product
urlpatterns =[
    path('product-list', views.ProductListView.as_view(), name='ProductListView'),
    path('product-detail/<str:slug>', views.ProductDetailView.as_view(), name='ProductDetailView'),
    path('product-create', views.ProductCreateView.as_view(), name='ProductCreateView'),
]