from django.db import connection
from apps.core.models.collection import Collection
from apps.core.schema.collection import CollectionSerializer


class CollectionRepository:
    @staticmethod
    def create(data):
        collection = Collection.objects.create(**data)
        return collection

    @staticmethod
    def get_all():
        collection_list = Collection.objects.all()
        return collection_list
    
    @staticmethod
    def get_by_sku(sku : str):
        try:
            return Collection.objects.get(sku=sku, is_deleted=False)
        except Collection.DoesNotExist:
            return None

    @staticmethod
    def update(collection, validated_data):
        serializer = CollectionSerializer(collection, data=validated_data, partial=True)
        serializer.is_valid(raise_exception=True)
        return serializer.save()

    @staticmethod
    def delete(collection):
        collection.is_deleted = True
        collection.save()
        return collection
