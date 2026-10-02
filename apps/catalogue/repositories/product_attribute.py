


from apps.catalogue.models.products import M2MProductAttribute


class ProductAttributeRepository:
    def create(self, product, attribute):
        return M2MProductAttribute.objects.create(
            product = product,
            attribute = attribute
        )
        
    def get_by_product(self, product):
        return M2MProductAttribute.objects.select_related('attribute').filter(product=product)
    
    
    
product_attribute_repository = ProductAttributeRepository()