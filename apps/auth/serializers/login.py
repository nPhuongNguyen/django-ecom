from rest_framework import serializers
class LoginInputSerializer(serializers.Serializer):
    user_email = serializers.CharField(max_length=100)
    user_password = serializers.CharField(max_length=100)
    remember_me = serializers.BooleanField(default=0)
