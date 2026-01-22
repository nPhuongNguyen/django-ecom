from rest_framework import serializers
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from ..models.categories import Category
from apps.catalogue.models.products import Product
from .product_variants import ProductVariantInProductSerializer, ProductVariantListSerializer
class ProductListSerializer(serializers.ModelSerializer):
    variants = ProductVariantInProductSerializer(many=True)
    category = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ['id','name', 'slug', 'description', 'price', 'is_active', 'img', 'category','variants']

    def get_category(self, obj):
        try:
            category = Category.objects.get(pk=obj.category.id)
            return {
                "id": category.id,
                "name": category.name
            }
        except:
            return ''
    
class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'description', 'is_active', 'price', 'category', 'img']

    def validate(self, attrs):
        if "name" in attrs:
            name = attrs["name"]
            slug_base = slugify(name)
            slug = slug_base

            counter = 1
            while Product.objects.filter(slug=slug).exclude(
                id=self.instance.id if self.instance else None
            ).exists():
                slug = f"{slug_base}-{counter}"
                counter += 1

            attrs["slug"] = slug

        return attrs

class ProductDetailSerializer(serializers.ModelSerializer):
    variants = ProductVariantInProductSerializer(many=True)
    category = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'is_active', 'price', 'category', 'slug', 'img', 'variants', 'updated_by']
    def get_category(self, obj):
        if obj.category:
            return {
                "id": obj.category.id,
                "name": obj.category.name
            }
        return None

class ProductUpdateSerializer(serializers.ModelSerializer):

    name = serializers.CharField(required = False)
    class Meta:
        model = Product
        fields = ['name', 'description', 'is_active', 'price', 'category', 'img']

    def validate(self, attrs):
        if "name" in attrs:
            name = attrs["name"]
            slug_base = slugify(name)
            slug = slug_base

            counter = 1
            while Product.objects.filter(slug=slug).exclude(
                id=self.instance.id if self.instance else None
            ).exists():
                slug = f"{slug_base}-{counter}"
                counter += 1

            attrs["slug"] = slug

        return attrs
        