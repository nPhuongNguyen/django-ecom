from django.urls import path
from apps.sales import views_api

urlpatterns = [
    path('order', views_api.OrderAPI.as_view(), name='order-api'),
    path('add-to-cart', views_api.CartAPI.as_view(), name='cart-api')
]
