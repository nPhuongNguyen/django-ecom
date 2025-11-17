from django.urls import path

from apps.catalogue import views_api
urlpatterns = [
    #product
    path('products-list',views_api.ProductListAPI.as_view(), name='ProductListAPI'),
    path('products-detail', views_api.ProductDetailAPI.as_view(), name= 'ProductDetailAPI'),
    path('products-create', views_api.ProductListAPI.as_view(), name='ProductCreateAPI'),

    #product variant
    path('product_variants',views_api.ProductVariantListAPI.as_view(),name='ProductVariantListAPI')
]