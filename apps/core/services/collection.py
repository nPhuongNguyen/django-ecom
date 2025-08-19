from apps.core.repositories.collection import CollectionRepository
from apps.core.schema.collection import CollectionSerializer
from apps.utils.decorator import *


class CollectionService:
    @staticmethod
    @catch_exceptions
    def create_collection(data: dict):
        collection = CollectionRepository.create(data)
        collection_validate_serializer = CollectionSerializer(collection)
        return collection_validate_serializer.data
    @staticmethod
    @catch_exceptions
    def get_collection_by_sku(sku):
        collection = CollectionRepository.get_by_sku(sku)
        if not collection:
            return None
        collection_validate_serializer = CollectionSerializer(collection)
        return collection_validate_serializer.data

    @staticmethod
    @catch_exceptions
    def get_all_collections():
        collection = CollectionRepository.get_all()
        collection_validate_serializer = CollectionSerializer(collection, many =True)
        return collection_validate_serializer.data

    @staticmethod
    @catch_exceptions
    def update_collection(sku: str, data: dict):
        collection = CollectionRepository.get_by_sku(sku)
        if not collection:
            return None
        update_collection = CollectionRepository.update(collection, data)
        collection_validate_serializer = CollectionSerializer(update_collection)
        return collection_validate_serializer.data

    @staticmethod
    @catch_exceptions
    def delete_collection(sku):
        collection = CollectionRepository.get_by_sku(sku)
        if not collection:
            return None
        delete_collection = CollectionRepository.delete(collection)
        collection_validate_serializer = CollectionSerializer(delete_collection)
        return collection_validate_serializer.data
