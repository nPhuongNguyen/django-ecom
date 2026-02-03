from rest_framework import serializers
class RegisterInputSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=100)
    password = serializers.CharField(max_length=100)
    confirm_password = serializers.CharField(max_length=100)

class RegisterConfirmInputSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=100)
    confirmation_code = serializers.CharField(max_length=10)