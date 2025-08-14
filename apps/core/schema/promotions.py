from rest_framework import serializers

from apps.core.models.promotions import Promotion
from apps.core.schema.categories import CategorySerializer
from apps.core.schema.collection import CollectionSerializer
from apps.core.schema.products import ProductOutputSerializer

class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = '__all__'
        read_only_fields = ['is_deleted']

class PromotionOutputSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many = True, read_only=True)
    collection = CollectionSerializer(many=True, read_only=True)
    product = ProductOutputSerializer(many = True, read_only = True)

    class Meta:
        model = Promotion
        fields = '__all__'