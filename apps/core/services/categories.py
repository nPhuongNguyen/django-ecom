from apps.core.repositories.categories import CategoryRepository


class CategoryService:
    @staticmethod
    def create_category(data):
        return CategoryRepository.create(data)

    @staticmethod
    def get_category_by_sku(sku):
        return CategoryRepository.get_by_sku(sku)

    @staticmethod
    def get_all_categories():
        return CategoryRepository.get_all()

    @staticmethod
    def update_category(sku, data):
        category = CategoryRepository.get_by_sku(sku)
        if not category:
            return None
        return CategoryRepository.update(category, data)

    @staticmethod
    def delete_category(slug):
        category = CategoryRepository.get_by_sku(slug)
        if not category:
            return None
        return CategoryRepository.delete(category)
