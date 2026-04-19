import email
from rest_framework import serializers

from django.contrib.auth.hashers import make_password

from ..models.user import User
class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['full_name', 'phone_number', 'email']

class UserCreateSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email already exists.")
        return email
    
    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        if password != confirm_password:
            raise serializers.ValidationError(
                {
                    "confirm_password": "Passwords do not match."
                }
            )
        return super().validate(attrs)
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)
    class Meta:
        model = User
        fields = ['email', 'password', 'confirm_password']

class UserDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['full_name', 'phone_number', 'email']

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['full_name', 'phone_number', 'email', 'is_active']


class UserConfirmSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['is_active']
