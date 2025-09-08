from rest_framework import serializers
from apps.core.models.products import Product
from apps.core.schema.categories import CategorySerializer
from apps.core.schema.collection import CollectionSerializer



class ProductSerializer(serializers.ModelSerializer):
    img = serializers.ImageField(required=False)
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['slug', 'is_deleted']


class ProductOutputSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    collection = CollectionSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = '__all__'
