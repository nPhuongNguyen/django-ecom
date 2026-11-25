from rest_framework import serializers
import unidecode
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from apps.catalogue.serializers.categories import CategoryInProduct
from apps.catalogue.models.products import Product, ProductVariant
from apps.catalogue.serializers.product_attribute import M2MProductAttributeSerializer

class ProductVariantInProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = [
            'id', 'name', 'img', 'sku',
            'price', 'stock_qty', 'is_active'
        ]   
        
class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','name', 'slug', 'description', 'is_active', 'img']
    
class ProductCreateSerializer(serializers.ModelSerializer):
    attributes = serializers.ListField(
        child=serializers.IntegerField(), 
        write_only=True, 
        required=False
    )
    class Meta:
        model = Product
        fields = ['name', 'description', 'is_active', 'category', 'img', 'attributes']

class ProductDetailSerializer(serializers.ModelSerializer):
    variants = ProductVariantInProductSerializer(many=True)
    category = CategoryInProduct(allow_null=True)
    attributes = M2MProductAttributeSerializer(many=True, source='product_attributes')
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'is_active', 'category', 'slug', 'img', 'variants', 'attributes', 'updated_by']

class ProductUpdateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required = False)
    class Meta:
        model = Product
        fields = ['name', 'description', 'is_active', 'category', 'img']
    
class ProductDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['is_deleted', 'deleted_at', 'deleted_by']
        
class ProductChangeStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['is_active']
        