

from rest_framework import serializers
from apps.catalogue.repositories.product_variant import product_variant_repository
class AddToCartSerializer(serializers.Serializer):
    product_variant_id = serializers.IntegerField()
    quantity = serializers.IntegerField()
    
class CartUpdateItemSerializer(serializers.Serializer):
    product_variant_id = serializers.IntegerField()
    quantity = serializers.IntegerField()
    
class CartDeleteItemSerializer(serializers.Serializer):
    product_variant_id = serializers.IntegerField()
    
class CartItemSerializer(serializers.Serializer):
    product_variant_id = serializers.IntegerField()
    quantity = serializers.IntegerField()
    
    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero.")
        return value
    
    def validate_product_variant_id(self, value):
        if not product_variant_repository.get_product_variant_by_id(value):
            raise serializers.ValidationError("Product variant does not exist.")
        return value