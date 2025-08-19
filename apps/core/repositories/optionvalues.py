from django.db import connection, transaction
from apps.core.models.products import *
from apps.utils import minio as S3
from datetime import datetime
from apps.utils.decorator import *

class OptionValueRepository:
    @staticmethod
    @catch_exceptions
    @log_sql
    def create(data: dict):
        option_value = OptionValue.objects.create(**data)
        return option_value
    
    @staticmethod
    @catch_exceptions
    @log_sql
    def get_all():
        option_value_list = list(OptionValue.objects.all())
        return option_value_list
    @staticmethod
    @catch_exceptions
    @log_sql
    def get_by_id(id : int):
        try:
            option_value = OptionValue.objects.get(id=id)
            return option_value
        except OptionValue.DoesNotExist:
            return None
    @staticmethod
    @catch_exceptions
    @log_sql
    def update(option_value: OptionValue, validated_data: dict):
        for attr, value in validated_data.items():
                setattr(option_value, attr, value)
        option_value.save()
        return option_value
    @staticmethod
    @catch_exceptions
    @log_sql
    def delete(id: int):
        try:
            obj = OptionValue.objects.get(id=id)
            obj.delete() 
            return True
        except OptionValue.DoesNotExist:
            return False
