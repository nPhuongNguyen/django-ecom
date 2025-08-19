from django.db import connection, transaction
from apps.core.models.products import Product
from apps.core.models.promotions import Promotion
from apps.core.schema.products import ProductSerializer
from apps.utils.decorator import *


class PromotionRepository:
    @staticmethod
    @catch_exceptions
    def create(data: dict):
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
    @catch_exceptions
    def get_all():
        promotion_list = Promotion.objects.all()
        return promotion_list
    @staticmethod
    @catch_exceptions
    def get_by_slug(slug : str):
        try:
            return Promotion.objects.get(slug=slug, is_activate=True)
        except Promotion.DoesNotExist:
            return None
    @staticmethod
    @catch_exceptions
    def update(promotion: Promotion, validated_data: dict):
        categories = validated_data.pop('category', [])
        collections = validated_data.pop('collection', [])
        products = validated_data.pop('product', [])
        with transaction.atomic():
            for attr, value in validated_data.items():
                setattr(promotion, attr, value)
            promotion.save()
            if categories:
                promotion.category.set(categories)

            if collections:
                promotion.collection.set(collections)
            
            if products:
                promotion.product.set(products)

        return promotion


    @staticmethod
    @catch_exceptions
    def delete(promotion: Promotion):
        promotion.is_activate = False
        promotion.save()
        return promotion
