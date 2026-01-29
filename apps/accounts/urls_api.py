
from django.urls import path

from apps.accounts import views_api

urlpatterns = [
    path('login', views_api.LoginAPI.as_view(), name="LoginAPI")
]
