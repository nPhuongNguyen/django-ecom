from apps.core.repositories.collection import CollectionRepository


class CollectionService:
    @staticmethod
    def create_collection(data):
        return CollectionRepository.create(data)

    @staticmethod
    def get_collection_by_sku(sku):
        return CollectionRepository.get_by_sku(sku)

    @staticmethod
    def get_all_collections():
        return CollectionRepository.get_all()

    @staticmethod
    def update_collection(sku, data):
        collection = CollectionRepository.get_by_sku(sku)
        if not collection:
            return None
        return CollectionRepository.update(collection, data)

    @staticmethod
    def delete_collection(sku):
        collection = CollectionRepository.get_by_sku(sku)
        if not collection:
            return None
        return CollectionRepository.delete(collection)
