


from apps.catalogue.models.products import M2MProductAttribute


class ProductAttributeRepository:
    def create_product_attribute(self, product, attribute):
        return M2MProductAttribute.objects.create(
            product = product,
            attribute = attribute
        )
    
product_attribute_repository = ProductAttributeRepository()