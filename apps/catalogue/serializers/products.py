from rest_framework import serializers
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from apps.catalogue.models.products import Product
from apps.utils.minio import S3Minio as S3
from apps.utils.utils_generate_unique_slug import generate_unique_slug
class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','name', 'slug', 'description', 'price', 'is_active', 'img', 'category']

class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'description', 'is_active', 'price', 'category', 'slug', 'img']
        read_only_fields = ['slug']

    def validate(self, attrs):
        name = attrs.get("name")
        attrs["slug"] = generate_unique_slug(Product, name)
        return attrs
class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'description', 'price', 'price', 'img', 'category']

class ProductUpdateSerializer(serializers.ModelSerializer):

    name = serializers.CharField(required = False)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, required = False)
    description = serializers.CharField(required = False)
    img = serializers.CharField(required = False)
    category = serializers.CharField(required = False)
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['slug']

    def validate(self, attrs):
        name = attrs.get("name")
        attrs["slug"] = generate_unique_slug(Product, name)
        return attrs
        