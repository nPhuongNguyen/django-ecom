from django.db import connection, transaction
from apps.core.models.collection import Collection
from apps.core.models.products import Product
from apps.core.schema.products import ProductSerializer


class ProductRepository:
    @staticmethod
    def create(data):
        collections = data.pop('collection', [])
        with transaction.atomic():
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
    def update(product, validated_data):
        category = validated_data.pop('category', None)
        collections = validated_data.pop('collection', None)
        Product.objects.filter(pk=product.pk).update(**validated_data)
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
