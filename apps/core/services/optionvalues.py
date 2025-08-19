from apps.core.repositories.options import OptionRepository
from apps.core.repositories.optionvalues import OptionValueRepository
from apps.core.repositories.products import ProductRepository
from apps.core.schema.options import OptionSerializer
from apps.core.schema.optionvalues import OptionValueOutputSerializer, OptionValueSerializer
from apps.core.schema.products import ProductOutputSerializer
from apps.utils.decorator import *


class OptionValueService:
    @staticmethod
    @catch_exceptions
    def create_option_value(data):
        option_value = OptionValueRepository.create(data)
        option_value_validate_serializer = OptionValueOutputSerializer(option_value)
        return option_value_validate_serializer.data

    
    @staticmethod
    @catch_exceptions
    def get_option_value_by_id(id: int):
        option_value =  OptionValueRepository.get_by_id(id)
        if option_value is None:
            return None
        option_value_validate_serializer = OptionValueOutputSerializer(option_value)
        return option_value_validate_serializer.data
    
    @staticmethod
    @catch_exceptions
    def get_all_options_value():
        option_value = OptionValueRepository.get_all()
        option_value_validate_serializer = OptionValueOutputSerializer(option_value, many = True)
        return option_value_validate_serializer.data
    @staticmethod
    @catch_exceptions
    def update_option_value(id: int, validated_data: dict):
        option_value = OptionValueRepository.get_by_id(id)
        if not option_value:
            return None
        update_option_value = OptionValueRepository.update(option_value, validated_data)
        option_value_validate_serializer = OptionValueOutputSerializer(update_option_value)
        return option_value_validate_serializer.data

    @staticmethod
    @catch_exceptions
    def delete_option_value(id : int):
        option_value = OptionValueRepository.get_by_id(id)
        if not option_value:
            return None
        delete_option_value = OptionValueRepository.delete(id)
        if delete_option_value is True:
            return True
        return None 
