
from django.urls import path

from apps.accounts import views

urlpatterns = [
    path('login', views.LoginView.as_view(), name="LoginView"),
    path('register', views.RegisterView.as_view(),name="RegisterView"),
    path('verify-otp/<str:email>', views.VerifyOTPView.as_view(),name="VerifyOTPView"),
]