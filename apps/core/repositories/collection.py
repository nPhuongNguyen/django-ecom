from django.db import connection
from apps.core.models.collection import Collection
from apps.core.schema.collection import CollectionSerializer
from apps.utils.decorator import *


class CollectionRepository:
    @staticmethod
    @catch_exceptions
    def create(data : dict):
        collection = Collection.objects.create(**data)
        return collection
    @staticmethod
    @catch_exceptions
    def get_all():
        collection_list = Collection.objects.all()
        return collection_list
    @staticmethod
    @catch_exceptions
    def get_by_sku(sku : str):
        try:
            return Collection.objects.get(sku=sku, is_deleted=False)
        except Collection.DoesNotExist:
            return None
    @staticmethod
    @catch_exceptions
    def update(collection: Collection, validated_data: dict):
        for attr, value in validated_data.items():
            setattr(collection, attr, value)
        collection.save()
        return collection
    @staticmethod
    @catch_exceptions
    def delete(collection: Collection):
        collection.is_deleted = True
        collection.save()
        return collection
