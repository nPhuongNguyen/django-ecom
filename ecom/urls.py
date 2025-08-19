"""
URL configuration for ecom project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from apps.core.views.categories import CategoryView
from apps.core.views.collection import CollectionView
from apps.core.views.option import OptionView
from apps.core.views.optionvalues import OptionValueView
from apps.core.views.products import ProductView
from apps.core.views.productvariants import ProductVariantView
from apps.core.views.promotions import PromotionView



urlpatterns = [
    #product
    path('products', ProductView.as_view()),
    path('products/<slug:slug>', ProductView.as_view()),
    #collection
    path('collections', CollectionView.as_view()),
    path('collections/<str:sku>', CollectionView.as_view()),
    #category
    path('categories', CategoryView.as_view()),
    path('categories/<str:sku>', CategoryView.as_view()),
    #promotion
    path('promotions',PromotionView.as_view()),
    path('promotions/<slug:slug>',PromotionView.as_view()),
    #productvariant
    path('productvariants',ProductVariantView.as_view()),
    path('productvariants/<str:sku>',ProductVariantView.as_view()),
    #option
    path('options',OptionView.as_view()),
    path('options/<int:id>',OptionView.as_view()),
    #optionvalue
    path('optionvalues',OptionValueView.as_view()),
    path('optionvalues/<int:id>', OptionValueView.as_view()),
]
