from rest_framework import serializers

from .attribute_value import AttributeValueListSerializer

from ..models.products import Attribute, M2MAttribute
class AttributeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = ['id', 'name', 'is_active']


class AttributeCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attribute
        fields = ['name', 'is_active']

class AttributeDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attribute
        fields = ['id', 'name', 'is_active']

class AttributeUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attribute
        fields = ['name', 'is_active']
