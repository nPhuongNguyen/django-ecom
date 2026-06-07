

from rest_framework import serializers

class ItemSerializer(serializers.Serializer):
    product_variant_id = serializers.IntegerField()
    quantity = serializers.IntegerField()
class CartItemSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    items = serializers.ListField(child=ItemSerializer())
    
class CartUpdateItemSerializer(serializers.Serializer):
    items = serializers.ListField(child=ItemSerializer())