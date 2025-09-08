from apps.core.repositories.options import OptionRepository
from apps.core.schema.options import OptionSerializer
from apps.utils.decorator import *


class OptionService:
    @staticmethod
    @catch_exceptions
    def create_option(data):
        option = OptionRepository.create(data)
        option_validate_serializer = OptionSerializer(option)
        return option_validate_serializer.data

    @staticmethod
    @catch_exceptions
    def get_option_by_id(id: int):
        option =  OptionRepository.get_by_id(id)
        if option is None:
            return None
        option_validate_serializer = OptionSerializer(option)
        return option_validate_serializer.data

    @staticmethod
    @catch_exceptions
    def get_all_options():
        option = OptionRepository.get_all()
        option_validate_serializer = OptionSerializer(option, many = True)
        return option_validate_serializer.data
    @staticmethod
    @catch_exceptions
    def update_option(id: int, validated_data: dict):
        option = OptionRepository.get_by_id(id)
        if not option:
            return None
        update_option = OptionRepository.update(option, validated_data)
        option_validate_serializer = OptionSerializer(update_option)
        return option_validate_serializer.data

    @staticmethod
    @catch_exceptions
    def delete_option(id : int):
        option = OptionRepository.get_by_id(id)
        if not option:
            return None
        delete_option = OptionRepository.delete(option)
        option_validate_serializer = OptionSerializer(delete_option)
        return option_validate_serializer.data
