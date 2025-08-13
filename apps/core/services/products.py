from apps.core.repositories.products import ProductRepository


class ProductService:
    @staticmethod
    def create_product(data):
        return ProductRepository.create(data)
