from django.db import transaction
from rest_framework.exceptions import ValidationError
from apps.catalogue.repositories.product_variant import product_variant_repository
from apps.catalogue.repositories.attribute_value import attribute_value_repository
from apps.catalogue.repositories.product_attribute import product_attribute_repository
from apps.catalogue.repositories.m2m_variant_attribute_value import m2m_variant_attribute_value_repository
from apps.catalogue.repositories.product import product_repository
from apps.catalogue.repositories.attribute import attribute_repository
from apps.catalogue.views_api import attribute_value

class ProductVariantService:
    def create(self, product_variant_data, attribute_value_list):
        attribute_value_list = attribute_value_list or []
        product = product_variant_data.get('product')
        list_attribute_by_product = product_repository.get_attribute_ids_by_product(product)
        list_attribute_by_attribute_value = attribute_value_repository.get_attribute_ids_by_attribute_value(attribute_value_list)
        if set(list_attribute_by_product) != set(list_attribute_by_attribute_value):
            raise ValidationError("Attribute values do not match the product's attributes.")
        for attribute_value_id in attribute_value_list:
            with transaction.atomic():
                attribute_value = attribute_value_repository.get_by_id(attribute_value_id)
                if not attribute_value:
                    raise ValidationError(f"Attribute value with ID {attribute_value_id} does not exist.")
                m2m_variant_attribute_value = m2m_variant_attribute_value_repository.create(attribute_value.attribute, attribute_value)
                product_variant_data.update({'m2m_variant_attribute_value': m2m_variant_attribute_value})
                product_variant_repository.create(product_variant_data) 
        return

product_variant_service = ProductVariantService()