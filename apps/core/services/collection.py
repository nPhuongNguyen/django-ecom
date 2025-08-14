from apps.core.repositories.collection import CollectionRepository


class CollectionService:
    @staticmethod
    def create_collection(data):
        return CollectionRepository.create(data)

    @staticmethod
    def get_collection_by_slug(slug):
        return CollectionRepository.get_by_slug(slug)

    @staticmethod
    def get_all_collections():
        return CollectionRepository.get_all()

    @staticmethod
    def update_collection(slug, data):
        collection = CollectionRepository.get_by_slug(slug)
        if not collection:
            return None
        return CollectionRepository.update(collection, data)

    @staticmethod
    def delete_collection(slug):
        collection = CollectionRepository.get_by_slug(slug)
        if not collection:
            return None
        return CollectionRepository.delete(collection)
