from django.urls import path
from apps.sales import views_api

urlpatterns = [
    path('order', views_api.OrderAPI.as_view(), name='order-api'),
    path('add-to-cart', views_api.CartCreateAPI.as_view(), name='cart-api'),
    path('cart-detail/<int:user_id>', views_api.CartDetailAPI.as_view(), name='cart-detail-api'),
    path('cart-update/<int:user_id>', views_api.CartUpdateAPI.as_view(), name='cart-update-api')
]
