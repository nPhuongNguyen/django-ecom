from django.urls import path
from apps.sales import views_api

urlpatterns = [
    path('orders/', views_api.OrderAPI.as_view(), name='order-api'),
]
