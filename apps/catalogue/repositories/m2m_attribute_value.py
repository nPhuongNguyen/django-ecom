


from apps.catalogue.models.products import M2MAttributeValue


class M2MAttributeValueRepository:
    def create(self, attribute, attribute_value):
        return M2MAttributeValue.objects.create(attribute=attribute, attribute_value=attribute_value)
    
m2m_attribute_value_repository = M2MAttributeValueRepository()