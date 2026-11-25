from rest_framework import serializers

from apps.catalogue.models.products import M2MProductAttribute
from apps.catalogue.serializers.attribute import AttributeDetailSerializer

class ProductAttributeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = M2MProductAttribute
        fields = ['product', 'attribute']
        
class ProductAttributeInputSerializer(serializers.Serializer):
    product = serializers.IntegerField()
    attributes = serializers.ListField(
        child = serializers.IntegerField(),
        allow_empty=False
    )
        
class ProductAttributeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = M2MProductAttribute
        fields = ['id', 'product', 'attribute', 'is_active']
        
class M2MProductAttributeSerializer(serializers.ModelSerializer):
    attribute = AttributeDetailSerializer()
    class Meta:
        model = M2MProductAttribute
        fields = ['id', 'attribute']
        