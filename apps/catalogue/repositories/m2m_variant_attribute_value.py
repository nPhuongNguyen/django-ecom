
from apps.catalogue.models.products import M2MVariantAttributeValue

class M2MVariantAttributeValueRepository:
    def get_by_id(self, attr_id):
        return M2MVariantAttributeValue.objects.filter(id=attr_id).first()
    
    def get_by_ids(self, attr_ids):
        return M2MVariantAttributeValue.objects.filter(id__in=attr_ids)
    
    def create(self, variant, m2m_attribute_value):
        return M2MVariantAttributeValue.objects.create(variant=variant, m2m_attribute_value=m2m_attribute_value)

m2m_variant_attribute_value_repository = M2MVariantAttributeValueRepository()