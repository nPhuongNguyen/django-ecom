from django.urls import path

from apps.accounts import views


#User
urlpatterns =[
    path('user-list', views.UserListView.as_view(), name='UserListView'),
]