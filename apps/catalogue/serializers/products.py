from rest_framework import serializers
import unidecode
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from apps.catalogue.serializers.categories import CategoryInProduct
from apps.catalogue.models.products import Product
from apps.catalogue.serializers.product_attribute import ProductAttributeInProductSerializer
from .product_variants import ProductVariantInProductSerializer
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
    product_attributes = ProductAttributeInProductSerializer(many=True)
    category = CategoryInProduct(allow_null=True)
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'is_active', 'category', 'slug', 'img', 'variants', 'product_attributes', 'updated_by']

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
        