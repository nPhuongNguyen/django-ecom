from django.db import transaction
from rest_framework.exceptions import ValidationError
from apps.catalogue.repositories.product_variant import product_variant_repository
from apps.catalogue.repositories.attribute_value import attribute_value_repository
from apps.catalogue.repositories.m2m_variant_attribute_value import m2m_variant_attribute_value_repository
from apps.catalogue.repositories.product import product_repository
from apps.catalogue.repositories.m2m_attribute_value import m2m_attribute_value_repository

class ProductVariantService:
    def create(self, product_variant_data, attribute_value_list):
        attribute_value_list = list(set(attribute_value_list or []))
        product = product_variant_data.get('product')
        with transaction.atomic():
            product_variant = product_variant_repository.create(product_variant_data)
            if attribute_value_list: 
                list_attribute_by_product = product_repository.get_attribute_ids_by_product(product)
                list_attribute_by_attribute_value = attribute_value_repository.get_attribute_ids_by_attribute_value(attribute_value_list)
                if set(list_attribute_by_product) != set(list_attribute_by_attribute_value):
                    raise ValidationError("Attribute values do not match the product's attributes.")
                for attribute_value_id in attribute_value_list:
                    attribute_value = attribute_value_repository.get_by_id(attribute_value_id)
                    if not attribute_value:
                        raise ValidationError(f"Attribute value with ID {attribute_value_id} does not exist.")
                    m2m_attribute_value = m2m_attribute_value_repository.create(attribute_value.attribute, attribute_value)
                    m2m_variant_attribute_value_repository.create(product_variant, m2m_attribute_value)
        return product_variant

product_variant_service = ProductVariantService()