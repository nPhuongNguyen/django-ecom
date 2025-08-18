from apps.core.repositories.products import ProductRepository
from apps.core.schema.products import ProductOutputSerializer


class ProductService:
    @staticmethod
    def create_product(data):
        product = ProductRepository.create(data)
        product_validate_serializer = ProductOutputSerializer(product)
        return product_validate_serializer.data

    @staticmethod
    def get_product_by_slug(slug):
        product =  ProductRepository.get_by_slug(slug)
        if product is None:
            return None
        product_validate_serializer = ProductOutputSerializer(product)
        return product_validate_serializer.data

    @staticmethod
    def get_all_products():
        product = ProductRepository.get_all()
        product_validate_serializer = ProductOutputSerializer(product, many = True)
        return product_validate_serializer.data
    
    @staticmethod
    def update_product(slug, validated_data):
        product = ProductRepository.get_by_slug(slug)
        if not product:
            return None
        update_product = ProductRepository.update(product, validated_data)
        product_validate_serializer = ProductOutputSerializer(update_product)
        return product_validate_serializer.data


    @staticmethod
    def delete_product(slug):
        product = ProductRepository.get_by_slug(slug)
        if not product:
            return None
        delete_product = ProductRepository.delete(product)
        product_validate_serializer = ProductOutputSerializer(delete_product)
        return product_validate_serializer.data
