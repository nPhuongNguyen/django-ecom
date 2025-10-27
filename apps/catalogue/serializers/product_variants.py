from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from apps.catalogue.models.products import ProductVariant


class ProductVariantListSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField() 
    class Meta:
        model = ProductVariant
        fields = ['name', 'img', 'sku', 'price', 'stock_qty', 'product']
    def get_product(self, obj):
        product = obj.product
        return {
            'name': product.name,
            'slug': product.slug
        }
    
class ProductVariantCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ['name', 'img', 'sku', 'price', 'stock_qty', 'product']

    def validate_sku(self, value):
        product = self.initial_data.get('product')
        if ProductVariant.objects.filter(sku = value, product_id = product).exists():
            raise serializers.ValidationError(_("SKU Product variant already exists."))
        return value
    
class ProductVariantDetailSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField() 
    class Meta:
        model = ProductVariant
        fields = ['name', 'img', 'sku', 'price', 'stock_qty', 'product']
    
    def get_product(self, obj):
        product = obj.product
        return {
            'name': product.name,
            'slug': product.slug
        }
    
class ProductVariantUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductVariant
        fields = ['name', 'img', 'sku', 'price', 'stock_qty', 'product']

    def validate_sku(self, value):
        product = self.initial_data.get('product')
        if ProductVariant.objects.filter(sku = value, product_id = product).exclude(id = self.initial.id).exists():
            raise serializers.ValidationError(_("SKU Product variant already exists."))
        return value