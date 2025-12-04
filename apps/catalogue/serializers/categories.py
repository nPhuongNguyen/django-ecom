from rest_framework import serializers

from apps.catalogue.models.categories import Category
class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'sku', 'is_active']