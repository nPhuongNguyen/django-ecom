
from apps.core.models.products import *
from apps.utils.decorator import *

class OptionRepository:
    @staticmethod
    @catch_exceptions
    @log_sql
    def create(data: dict):
        option = Option.objects.create(**data)
        return option

    @staticmethod
    @catch_exceptions
    @log_sql
    def get_all():
        option_list = list(Option.objects.all())
        return option_list
    @staticmethod
    @catch_exceptions
    @log_sql
    def get_by_id(id : int):
        try:
            option = Option.objects.get(id=id, is_deleted=False)
            return option
        except Option.DoesNotExist:
            return None
    @staticmethod
    @catch_exceptions
    @log_sql
    def update(option: Option, validated_data: dict):
        for attr, value in validated_data.items():
            setattr(option, attr, value)
        option.save()
        return option
    @staticmethod
    @catch_exceptions
    @log_sql
    def delete(option: Option):
        option.is_deleted = True
        option.save()
        return option
