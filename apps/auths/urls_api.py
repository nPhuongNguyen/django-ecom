from django.urls import path
from apps.auths import views_api
urlpatterns = [
    #User
    path('users',views_api.UserListAPI.as_view(), name='UserListAPI'),
    path('user-detail', views_api.UserDetailAPI.as_view(), name= 'UserDetailAPI'),
]