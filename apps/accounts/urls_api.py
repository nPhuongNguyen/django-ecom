
from django.urls import path

from apps.accounts import views_api

urlpatterns = [
    path('login', views_api.LoginAPI.as_view(), name="LoginAPI"),
    path('register', views_api.RegisterAPI.as_view(),name="RegisterAPI"),
    path('register-confirm', views_api.RegisterConfirmAPI.as_view(),name="RegisterConfirmAPI"),
    #Send Mail
    path('send-mail', views_api.SendMailAPIView.as_view(), name='SendMailAPI'),
]
