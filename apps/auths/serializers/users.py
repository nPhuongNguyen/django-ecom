from rest_framework import serializers

from apps.auths.models.users import Users

class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = ['full_name', 'phone_number', 'email']

class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = ['full_name', 'phone_number', 'email']

class UserDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = ['full_name', 'phone_number', 'email']

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['full_name', 'phone_number', 'email']
