from apps.core.repositories.categories import CategoryRepository
from apps.core.schema.categories import CategorySerializer


class CategoryService:
    @staticmethod
    def create_category(data: dict):
        category = CategoryRepository.create(data)
        category_validate_serializer = CategorySerializer(category)
        return category_validate_serializer.data
    
    @staticmethod
    def get_category_by_id(id : int):
        category = CategoryRepository.get_by_id(id)
        if not category:
            return None
        category_validate_serializer = CategorySerializer(category)
        return category_validate_serializer.data


    @staticmethod
    def get_category_by_sku(sku: str):
        category = CategoryRepository.get_by_sku(sku)
        if not category:
            return None
        category_validate_serializer = CategorySerializer(category)
        return category_validate_serializer.data

    @staticmethod
    def get_all_categories():
        category =  CategoryRepository.get_all()
        category_validate_serializer = CategorySerializer(category, many = True)
        return category_validate_serializer.data

    @staticmethod
    def update_category(sku: str, data: dict):
        category = CategoryRepository.get_by_sku(sku)
        if not category:
            return None
        update_category = CategoryRepository.update(category, data)
        category_validate_serializer = CategorySerializer(update_category)
        return category_validate_serializer.data

    @staticmethod
    def delete_category(slug):
        category = CategoryRepository.get_by_sku(slug)
        if not category:
            return None
        delete_category = CategoryRepository.delete(category)
        category_validate_serializer = CategorySerializer(delete_category)
        return category_validate_serializer.data
