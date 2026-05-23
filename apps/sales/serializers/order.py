

from rest_framework import serializers

from apps.sales.model.order import Order

class OrderItemsCreateInputSerializer(serializers.Serializer):
    product_variant_id = serializers.IntegerField()
    quantity = serializers.IntegerField()

class OrderCreateInputSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    items = serializers.ListField(
        child=OrderItemsCreateInputSerializer(),
        allow_empty=False
    )
    note = serializers.CharField(required=False, allow_blank=True)
    total_amount = serializers.IntegerField(default=0)
    subtotal_amount = serializers.IntegerField(default=0)
    discount_amount = serializers.IntegerField(default=0)
    
class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"