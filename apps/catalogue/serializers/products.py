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
        fields = ['name', 'description', 'is_active', 'image', 'price', 'category','slug']
        read_only_fields = ['slug']

    def validate(self, attrs):
        name = attrs.get("name")
        slug = slugify(name)

        if Product.objects.filter(name=name).exists():
            raise serializers.ValidationError({"name": _("Name already exists.")})

        if Product.objects.filter(slug=slug).exists():
            raise serializers.ValidationError({"name": _("Slug already exists.")})
        attrs["slug"] = slug
        return attrs

    
    def create(self, validated_data):
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
        fields = ['id', 'name', 'slug', 'description', 'price', 'price', 'img', 'category']
        read_only_fields = ['slug']
        
class ProductUpdateSerializer(serializers.ModelSerializer):
    image = serializers.FileField(default = None)
    image_check = serializers.IntegerField()
    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'description', 'price', 'price', 'image', 'image_check', 'category']
        read_only_fields = ['slug']

    def validate(self, attrs):
        name = attrs.get("name")
        slug = slugify(name)
        product_id = self.instance.id if self.instance else None
        
        if Product.objects.filter(name=name).exclude(id=product_id).exists():
            raise serializers.ValidationError({"name": _("Name already exists.")})

        if Product.objects.filter(slug=slug).exclude(id=product_id).exists():
            raise serializers.ValidationError({"name": _("Slug already exists.")})
        return attrs
           
    def update(self, instance, validated_data):
        new_name = validated_data.get('name', instance.name)
        if new_name != instance.name:
            instance.slug = slugify(new_name)

        image_check = validated_data.pop('image_check')
        image = validated_data.pop('image')
        if image_check == 1:
            validated_data['img'] = None
            if(image):
                img_url = S3.minio_upload_file(file=image, file_name=image.name)
                if img_url is None:
                    raise serializers.ValidationError({
                        "image": _("Upload error")
                    })
                validated_data['img'] = img_url
        return super().update(instance, validated_data)