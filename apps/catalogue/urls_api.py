from django.urls import path

from apps.catalogue import views_api
urlpatterns = [
    #product
    path('product-list',views_api.ProductListAPI.as_view(), name='ProductListAPI'),
    path('product-detail/<str:pk>',views_api.ProductDetailAPI.as_view(), name='ProductDetailAPI'),
    path('product-create', views_api.ProductCreateAPI.as_view(), name='ProductCreateAPI'),
    path('product-update/<str:pk>', views_api.ProductUpdateAPI.as_view(), name= 'ProductUpdateAPI'),
    path('product-change-status/<str:pk>', views_api.ProductChangeStatusAPI.as_view(), name='ProductChangeStatusAPI'),
    path('product-destroy', views_api.ProductDestroyAPI.as_view(), name ='ProductDestroyAPI'),

    #product variant
    path('product-variant-list',views_api.ProductVariantListAPI.as_view(), name='ProductVariantListAPI'),
    path('product-variant-create', views_api.ProductVariantCreateAPI.as_view(), name='ProductVariantCreateAPI'),
    path('product-variant-update/<str:pk>',views_api.ProductVariantUpdateAPI.as_view(), name='ProductVariantUpdateAPI'),
    path('product-variant-change-status/<str:pk>', views_api.ProductVariantChangeStatusAPI.as_view(), name='ProductVariantChangeStatusAPI'),
    path('product-variant-destroy',views_api.ProductVariantDestroyAPI.as_view(), name='ProductVariantDestroyAPI'),


    #category
    path('category-list', views_api.CategoryListAPI.as_view(), name='CategoryListAPI'),

    #upload image
    path('upload-image', views_api.UploadImageAPI.as_view(), name='UploadImageAPI'),
]