from django.db import connection, transaction
from apps.core.models.products import Product
from apps.core.models.promotions import Promotion
from apps.core.schema.products import ProductSerializer


class PromotionRepository:
    @staticmethod
    def create(data):
        products = data.pop('product', [])
        categories = data.pop('category', [])
        collections = data.pop('collection', [])
        with transaction.atomic():
            promotion = Promotion.objects.create(**data)
            if products:
                promotion.product.set(products)
            if categories:
                promotion.category.set(categories)
            if collections:
                promotion.collection.set(collections)
        return promotion
            
    @staticmethod
    def get_all():
        promotion_list = Promotion.objects.all()
        return promotion_list
    
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
        with transaction.atomic():
            serializer = ProductSerializer(product, data=validated_data, partial=True)
            serializer.is_valid(raise_exception=True)
            updated_product = serializer.save()

            if category is not None:
                updated_product.category = category
                updated_product.save(update_fields=['category'])

            if collections is not None:
                updated_product.collection.set(collections)

        return updated_product



    @staticmethod
    def delete(product):
        product.is_deleted = True
        product.save()
        return product
