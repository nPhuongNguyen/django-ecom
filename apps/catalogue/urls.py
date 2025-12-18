from django.urls import path

from apps.catalogue import views

#Product
urlpatterns =[
    path('product-list', views.ProductListView.as_view(), name='ProductListView'),
    path('product-detail/<str:slug>', views.ProductDetailView.as_view(), name='ProductDetailView'),
    path('product-create', views.ProductCreateView.as_view(), name='ProductCreateView'),
]

#Product Variant
urlpatterns +=[
    path('product-variant-list', views.ProductVariantListView.as_view(), name='ProductVariantListView'),
    path('product-variant-detail/<str:pk>', views.ProductVariantDetailView.as_view(), name='ProductVariantDetailView'),
]

#Attribute

urlpatterns +=[
    path('attribute-list', views.AttributeListView.as_view(), name='AttributeListView'),
    path('attribute-detail/<str:pk>',views.AttributeDetailView.as_view(), name='AttributeDetailView'),
    path('attribute-create',views.AttributeCreateView.as_view(), name='AttributeCreateView'),
]
