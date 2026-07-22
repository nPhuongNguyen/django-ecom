from rest_framework import serializers

from apps.catalogue.models.products import Attribute, M2MProductAttribute

class ProductAttributeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = M2MProductAttribute
        fields = ['product', 'attribute']
        
class AttributeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = ['id', 'name', 'is_active']
        
class ProductAttributeInProductSerializer(serializers.ModelSerializer):
    attribute = AttributeDetailSerializer(read_only=True)
    class Meta:
        model = M2MProductAttribute
        fields = ['id', 'attribute', 'is_active']
        
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
        