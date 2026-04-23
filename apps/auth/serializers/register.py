from rest_framework import serializers

class RegisterConfirmInputSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=100)
    confirmation_code = serializers.CharField(max_length=10)

class RegisterResendOTPInputSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=100)