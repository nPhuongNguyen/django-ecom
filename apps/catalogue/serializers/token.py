from rest_framework import serializers

class InfoTokenSerializer(serializers.Serializer):
    iat = serializers.IntegerField()
    exp = serializers.IntegerField()
    jti = serializers.UUIDField()