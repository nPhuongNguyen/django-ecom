from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from apps.catalogue.models.products import Product, ProductVariant


class ProductVariantListSerializer(serializers.ModelSerializer): 
    product = serializers.SerializerMethodField()
    class Meta:
        model = ProductVariant
        fields = ['id', 'name', 'img', 'sku', 'price', 'stock_qty', 'product', 'is_active']

    def get_product(self, obj):
        try:
            product = Product.objects.get(pk=obj.product.id)
            return {
                'id': product.id,
                'name': product.name,
                'slug': product.slug
            }
        except:
            return ''
    
class ProductVariantCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ['name', 'img', 'sku', 'price', 'stock_qty', 'product', 'is_active']
        read_only = ['sku']

    def validate_sku(self, value):
        product = self.initial_data.get('product')
        if ProductVariant.objects.filter(sku = value, product_id = product).exists():
            raise serializers.ValidationError(_("product variant with this sku already exists."))
        return value
    
class ProductVariantDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ['id', 'name', 'img', 'sku', 'price', 'stock_qty', 'product', 'is_active']
    
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