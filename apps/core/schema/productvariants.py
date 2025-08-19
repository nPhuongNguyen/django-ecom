from rest_framework import serializers
from apps.core.models.products import ProductVariant
from apps.core.schema.products import ProductOutputSerializer
class ProductVariantSerializer(serializers.ModelSerializer):
    img = serializers.ImageField(required=False)
    class Meta:
        model = ProductVariant
        fields = '__all__'
        read_only_fields = ['sku', 'is_deleted']

class ProductVariantInputSerializer(serializers.ModelSerializer):
    img = serializers.ImageField(required=False)
    class Meta:
        model = ProductVariant
        fields = '__all__'
        read_only_fields = ['is_deleted']

class ProductVariantOutputSerializer(serializers.ModelSerializer):
    product = ProductOutputSerializer(read_only=True)
    class Meta:
        model = ProductVariant
        fields = '__all__'
