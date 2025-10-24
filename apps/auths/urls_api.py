from django.urls import path
from apps.auths import views_api
urlpatterns = [
    path('users',views_api.UserListAPI.as_view(), name='UserListAPI')
]