
from django.urls import path
from apps.shared import views_api
urlpatterns = [
    path('health-check', views_api.HealthCheckAPIView.as_view(), name='HealthCheckAPIView'),
]