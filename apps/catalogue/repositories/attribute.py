

from apps.catalogue.models.products import Attribute, Product


class AttributeRepository:
    def get_by_id(self, attr_id):
        return Attribute.objects.filter(id=attr_id).first()
    
    def get_by_ids(self, attr_ids):
        return Attribute.objects.filter(id__in=attr_ids) 
    
attribute_repository = AttributeRepository()