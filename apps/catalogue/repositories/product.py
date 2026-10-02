

from apps.catalogue.models.products import Product


class ProductRepository:
    def create(self, product_data):
        return Product.objects.create(**product_data)
    def get_by_id(self, product_id):
        return Product.objects.filter(id=product_id).first()
    
    def get_attribute_ids_by_product(self, product: Product):
        return product.attributes.values_list('id', flat=True)

product_repository = ProductRepository()