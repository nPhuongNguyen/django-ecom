from django.db import connection, transaction
from apps.core.models.products import Product
from apps.core.schema.products import ProductSerializer
from apps.utils import minio as S3
from datetime import datetime

class ProductRepository:
    @staticmethod
    def create(data: dict):
        collections = data.pop('collection', [])
        with transaction.atomic():
            if data.get("img"):
                img_name = "img_product_" + datetime.now().strftime("%Y%m%d%H%M%S")
                img_url = S3.upload_image(data["img"], img_name)
                data["img"] = img_url 
            product = Product.objects.create(**data)
            if collections:
                product.collection.set(collections)
        return product

    @staticmethod
    def get_all():
        product_list = Product.objects.all()
        return product_list
    
    @staticmethod
    def get_by_slug(slug : str):
        try:
            return Product.objects.get(slug=slug, is_deleted=False)
        except Product.DoesNotExist:
            return None

    @staticmethod
    def update(product: Product, validated_data: dict):
        category = validated_data.pop('category', None)
        collections = validated_data.pop('collection', None)
        img_file = validated_data.pop("img", None)
        if img_file is not None:
            img_name = "img_product_" + datetime.now().strftime("%Y%m%d%H%M%S")
            img_url = S3.upload_image(img_file, img_name)
            product.img = img_url
        with transaction.atomic():
            for attr, value in validated_data.items():
                setattr(product, attr, value)
            if category is not None:
                product.category = category
            product.save() 
            if collections is not None:
                product.collection.set(collections)
        return product

    @staticmethod
    def delete(product):
        product.is_deleted = True
        product.save()
        return product
