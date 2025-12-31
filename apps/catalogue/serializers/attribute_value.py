from rest_framework import serializers

from ..models.products import AttributeValue
class AttributeValueListSerializer(serializers.ModelSerializer):

    class Meta:
        model = AttributeValue
        fields = ['id', 'name', 'is_active']

class AttributeValueCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = AttributeValue
        fields = ['name', 'is_active']

class AttributeValueDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = AttributeValue
        fields = ['id', 'name', 'is_active']

class AttributeValueUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = AttributeValue
        fields = ['name', 'is_active']
