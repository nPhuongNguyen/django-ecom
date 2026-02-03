
from django.urls import path

from apps.accounts import views_api

urlpatterns = [
    path('login', views_api.LoginAPI.as_view(), name="LoginAPI"),
    path('register', views_api.RegisterAPI.as_view(),name="RegisterAPI")
]
