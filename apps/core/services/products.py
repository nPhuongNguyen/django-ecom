from apps.core.repositories.products import ProductRepository


class ProductService:
    @staticmethod
    def create_product(data):
        return ProductRepository.create(data)

    @staticmethod
    def get_product_by_slug(slug):
        return ProductRepository.get_by_slug(slug)

    @staticmethod
    def get_all_products():
        return ProductRepository.get_all()
    
    @staticmethod
    def update_product(slug, data):
        product = ProductRepository.get_by_slug(slug)
        if not product:
            return None
        return ProductRepository.update(product, data)

    @staticmethod
    def delete_product(slug):
        product = ProductRepository.get_by_slug(slug)
        if not product:
            return None
        return ProductRepository.delete(product)
