from django.db import connection
from apps.core.models.categories import Category
from apps.core.schema.categories import CategorySerializer


class CategoryRepository:
    @staticmethod
    def create(data):
        category = Category.objects.create(**data)
        return category

    @staticmethod
    def get_all():
        category_list = Category.objects.all()
        return category_list
    
    @staticmethod
    def get_by_sku(sku : str):
        try:
            return Category.objects.get(sku=sku, is_deleted=False)
        except Category.DoesNotExist:
            return None

    @staticmethod
    def update(category, validated_data):
        serializer = CategorySerializer(category, data=validated_data, partial=True)
        serializer.is_valid(raise_exception=True)
        return serializer.save()

    @staticmethod
    def delete(category):
        category.is_deleted = True
        category.save()
        return category
