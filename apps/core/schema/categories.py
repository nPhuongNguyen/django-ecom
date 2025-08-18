from rest_framework import serializers
from apps.core.models.categories import Category



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ['sku', 'is_deleted']