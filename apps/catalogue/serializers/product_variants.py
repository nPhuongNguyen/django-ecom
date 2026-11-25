from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from apps.catalogue.models.products import M2MAttributeValue, M2MVariantAttributeValue, Product, ProductVariant
from apps.catalogue.serializers.attribute import AttributeDetailSerializer
from apps.catalogue.serializers.attribute_value import AttributeValueDetailSerializer
  
class M2MAttributeValueSerializer(serializers.ModelSerializer):
    attribute = AttributeDetailSerializer()
    attribute_value = AttributeValueDetailSerializer()

    class Meta:
        model = M2MAttributeValue
        fields = [
            'id',
            'attribute',
            'attribute_value',
        ]
  
class M2MVariantAttributeValueSerializer(serializers.ModelSerializer):
    m2m_attribute_value = M2MAttributeValueSerializer()

    class Meta:
        model = M2MVariantAttributeValue
        fields = [
            'id',
            'm2m_attribute_value',
        ]

class ProductInProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'description', 'is_active']
        
class ProductVariantListSerializer(serializers.ModelSerializer): 
    product = ProductInProductVariantSerializer()
    class Meta:
        model = ProductVariant
        fields = ['id', 'name', 'img', 'sku', 'price', 'stock_qty', 'product', 'is_active']
          
class ProductVariantCreateSerializer(serializers.ModelSerializer):
    attribute_value_list = serializers.ListField(child=serializers.IntegerField(), required=False, allow_empty=True)
    class Meta:
        model = ProductVariant
        fields = ['name', 'img', 'sku', 'price', 'stock_qty', 'product', 'is_active', 'attribute_value_list']

    def validate_sku(self, value):
        product = self.initial_data.get('product')
        if ProductVariant.objects.filter(sku = value, product_id = product).exists():
            raise serializers.ValidationError(_("product variant with this sku already exists."))
        return value
    
class ProductVariantDetailSerializer(serializers.ModelSerializer):
    product = ProductInProductVariantSerializer()
    variant_attribute_values = M2MVariantAttributeValueSerializer(
        many=True
    )
    class Meta:
        model = ProductVariant
        fields = ['id', 'name', 'img', 'sku', 'price', 'stock_qty', 'is_active', 'product', 'variant_attribute_values', 'updated_by']

class ProductVariantUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductVariant
        fields = ['name', 'img', 'sku', 'price', 'stock_qty', 'product', 'is_active']

    def validate_sku(self, value):
        product_id = self.initial_data.get('product') or self.instance.product_id
        print("self.instance",self.instance)
        if ProductVariant.objects.filter(sku = value, product_id = product_id).exclude(id = self.instance.id).exists():
            raise serializers.ValidationError(_("product variant with this sku already exists."))
        return value