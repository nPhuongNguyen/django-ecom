from django.db import connection
from apps.core.models.categories import Category
from apps.core.schema.categories import CategorySerializer
from apps.utils.decorator import *


class CategoryRepository:
    @staticmethod
    @catch_exceptions
    @log_sql
    def create(data):
        category = Category.objects.create(**data)
        return category
    @staticmethod
    @catch_exceptions
    @log_sql
    def get_all():
        category_list = Category.objects.all()
        return category_list
    @staticmethod
    @catch_exceptions
    @log_sql
    def get_by_sku(sku : str):
        try:
            return Category.objects.get(sku=sku, is_deleted=False)
        except Category.DoesNotExist:
            return None
    @staticmethod
    @catch_exceptions
    @log_sql
    def update(category : Category, validated_data: dict):
        for attr, value in validated_data.items():
            setattr(category, attr, value)
        category.save()
        return category
    @staticmethod
    @catch_exceptions
    @log_sql
    def delete(category: Category):
        category.is_deleted = True
        category.save()
        return category
