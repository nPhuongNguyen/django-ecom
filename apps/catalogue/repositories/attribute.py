

from apps.catalogue.models.products import Attribute


class AttributeRepository:
    def get_attribute_by_id(self, attr_id):
        return Attribute.objects.filter(id=attr_id).first()
    
attribute_repository = AttributeRepository()