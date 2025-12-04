from rest_framework import serializers

class InfoTokenSerializer(serializers.Serializer):
    user_name = serializers.CharField()
    user_phone = serializers.CharField()
    email = serializers.CharField()