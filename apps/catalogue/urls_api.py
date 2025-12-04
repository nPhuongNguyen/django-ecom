from django.urls import path

from apps.catalogue import views_api
urlpatterns = [
    #product
    path('product-list',views_api.ProductListAPI.as_view(), name='ProductListAPI'),
    path('product-update/<str:pk>', views_api.ProductUpdateAPI.as_view(), name= 'ProductUpdateAPI'),
    path('product-create', views_api.ProductCreateAPI.as_view(), name='ProductCreateAPI'),
    path('product-destroy', views_api.ProductDestroyAPI.as_view(), name ='ProductDestroyAPI'),
    path('product-change-status/<str:pk>', views_api.ProductChangeStatusAPI.as_view(), name='ProductChangeStatusAPI'),
    #product variant
    path('product_variants',views_api.ProductVariantListAPI.as_view(),name='ProductVariantListAPI'),


    #category
    path('category-list', views_api.CategoryListAPI.as_view(), name='CategoryListAPI'),

    #upload image
    path('upload-image', views_api.UploadImageAPI.as_view(), name='UploadImageAPI'),
]