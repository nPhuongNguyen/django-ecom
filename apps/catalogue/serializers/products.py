from rest_framework import serializers
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from apps.catalogue.models.products import Product
from apps.utils.minio import S3Minio as S3
class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','name', 'slug', 'description', 'price', 'is_active', 'img', 'category']

class ProductCreateSerializer(serializers.ModelSerializer):
    image = serializers.FileField(default = None)
    class Meta:
        model = Product
        fields = ['name', 'slug', 'description', 'is_active', 'image', 'price', 'category']

    def validate_name(self, value):
        if Product.objects.filter(name=value).exists():
            raise serializers.ValidationError(_("Name already exists."))
        return value
    
    def create(self, validated_data):
        if not validated_data.get('slug'):
            validated_data['slug'] = slugify(validated_data.get('name', ''))
        image = validated_data.pop('image', None)
        if image == None:
            validated_data['img'] = None
        else:
            img_url = S3.minio_upload_file(file=image, file_name=image.name)
            if img_url is None:
                raise serializers.ValidationError({
                    "image": _("Upload error")
                })
            validated_data['img'] = img_url
            
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