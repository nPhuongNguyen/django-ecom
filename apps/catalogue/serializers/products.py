from rest_framework import serializers
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from apps.catalogue.models.products import Product
class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','name', 'slug', 'description', 'price', 'img', 'category']

class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'slug', 'description', 'is_active', 'price', 'img', 'category']

    def validate_name(self, value):
        if Product.objects.filter(name=value).exists():
            raise serializers.ValidationError(_("Name already exists."))
        return value
    
    def create(self, validated_data):
        if not validated_data.get('slug'):
            validated_data['slug'] = slugify(validated_data.get('name', ''))
        return super().create(validated_data)
class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'slug', 'description', 'price', 'price', 'img', 'category']
        read_only_fields = ['slug']
        
class ProductUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'slug', 'description', 'price', 'price', 'img', 'category']
        read_only_fields = ['slug']

    def validate_name(self, value):
        if Product.objects.filter(name=value).exclude(id = self.initial.id).exists():
            raise serializers.ValidationError(_("Name already exists."))
        return value
           
    def update(self, instance, validated_data):
        new_name = validated_data.get('name', instance.name)
        if new_name != instance.name:
            instance.slug = slugify(new_name)
        return super().update(instance, validated_data)