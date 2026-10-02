

from apps.catalogue.models.products import AttributeValue


class AttributeValueRepository:
    def get_by_id(self, attr_value_id):
        return AttributeValue.objects.filter(id=attr_value_id).first()
    
    def get_attribute_ids_by_attribute_value(self, attribute_values):
        return AttributeValue.objects.filter(id__in=attribute_values).values_list('attribute_id', flat=True)

    def create(self, attribute, value):
        return AttributeValue.objects.create(attribute=attribute, name=value)
    
    
attribute_value_repository = AttributeValueRepository()