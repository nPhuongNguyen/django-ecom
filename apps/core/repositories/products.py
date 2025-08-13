from django.db import connection
from apps.core.models.products import Product
from apps.core.schema import ProductSerializer


class ProductRepository:
    @staticmethod
    def create(data):
        product = Product.objects.create(**data)
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
        serializer = ProductSerializer(product, data=validated_data, partial=True)
        serializer.is_valid(raise_exception=True)
        return serializer.save()

    @staticmethod
    def delete(product):
        product.is_deleted = True
        product.save()
        return product
