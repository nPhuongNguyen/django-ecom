

from apps.catalogue.models.products import Product


class ProductRepository:
    def create_product(self, product_data):
        product = Product.objects.create(**product_data)
        return product

product_repository = ProductRepository()