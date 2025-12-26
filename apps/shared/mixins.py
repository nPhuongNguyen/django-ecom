__all__ = [
    'BaseMixin',
    'ListMixin',
    'CreateMixin',
    'RetrieveMixin',
    'UpdateMixin',
    'DestroyMixin',
]

from datetime import datetime
from rest_framework import serializers
from rest_framework.generics import GenericAPIView
from apps.shared.models import BaseModelCreated, BaseModelUpdated, BaseModelDeleted
from apps.shared.response import ResponseBuilder, ResponseCodes
from django.db import transaction
from django.utils import timezone
class BaseMixin(GenericAPIView):
    serializer_class_list: serializers.Serializer
    serializer_class_create: serializers.Serializer
    serializer_class_detail: serializers.Serializer
    serializer_class_update: serializers.Serializer

    def get_serializer_class_list(self):
        serializer_cls = getattr(self, 'serializer_class_list', None)
        if serializer_cls is None:
            return None
        return serializer_cls

    def get_serializer_class_create(self):
        serializer_cls = getattr(self, 'serializer_class_create', None)
        if serializer_cls is None:
            return None
        return serializer_cls


    def get_serializer_class_detail(self):
        serializer_cls = getattr(self, 'serializer_class_detail', None)
        if serializer_cls is None:
            return None
        return serializer_cls

    def get_serializer_class_update(self):
        serializer_cls = getattr(self, 'serializer_class_update', None)
        if serializer_cls is None:
            return None
        return serializer_cls

    def get_request_data(self) -> dict:
        return getattr(self.request, 'data', {})
    
    def get_request_info_user(self) -> dict:
        user_info = getattr(self.request, 'data_decode_token', {})
        info_email = user_info.get('email', "")
        return info_email
    
    def check_info(self, lookup_value=None):
        if lookup_value is None:
            lookup_value = self.kwargs.get('pk')
        obj = self.get_queryset().filter(pk=lookup_value).first()
        return obj 


    def query_params(self):
        return getattr(self.request, 'query_params', {})

    class Meta:
        abstract = True


class ListMixin(BaseMixin):
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset().filter())
        page = self.paginate_queryset(queryset)
        serializer_class = self.get_serializer_class_list()
        if not serializer_class:
            return ResponseBuilder.build(
            code=ResponseCodes.SYSTEM_ERROR,
            errors="Serializer not found."
        )
        if page is not None:
            serializer = serializer_class(
                page, many=True
            )
            return self.get_paginated_response(serializer.data)

        serializer = serializer_class(
            queryset, many=True
        )
        return ResponseBuilder.build(
            code=ResponseCodes.SUCCESS,
            data=serializer.data
        )

class CreateMixin(BaseMixin):
    def get_create_data(self):
        return self.get_request_data()
    
    def get_context_created(self):
        user_email = self.get_request_info_user()
        return {
            'created_by' : user_email,
            'updated_by': user_email,
        }
       
    def create(self, request, *args, **kwargs):
        serializer_create = self.get_serializer_class_create()
        serializer_detail = self.get_serializer_class_detail()


        if not serializer_create or not serializer_detail:
            return ResponseBuilder.build(
                code=ResponseCodes.SYSTEM_ERROR,
                errors="Serializer not found."
            )

        serializer = serializer_create(
            data=self.get_create_data())
        if not serializer.is_valid():
            return ResponseBuilder.build(
                code=ResponseCodes.INVALID_INPUT,
                errors=serializer.errors
            )

        instance = serializer.save(**self.get_context_created())
        return ResponseBuilder.build(
            code=ResponseCodes.SUCCESS,
            data=serializer_detail(instance=instance).data
        )

class UpdateMixin(BaseMixin):
    def get_update_data(self):
        return self.get_request_data()
    
    def get_context_updated(self):
        user_email = self.get_request_info_user()
        return {
            'updated_by': user_email,
        }

    def update(self, request, *args, **kwargs):
        serializer_update = self.get_serializer_class_update()
        serializer_detail = self.get_serializer_class_detail()
        if not serializer_update or not serializer_detail:
            return ResponseBuilder.build(
                code=ResponseCodes.SYSTEM_ERROR,
                errors="Serializer not found."
            )
        
        instance = self.check_info()
        if not instance:
            return ResponseBuilder.build(
                code=ResponseCodes.INVALID_INPUT
            )
        serializer = serializer_update(
            instance=instance, data=self.get_update_data(), partial=True
        )
        if not serializer.is_valid():
            return ResponseBuilder.build(
                code=ResponseCodes.INVALID_INPUT,
                errors=serializer.errors
            )
        instance_sr = serializer.save(**self.get_context_updated())
        return ResponseBuilder.build(
            code=ResponseCodes.SUCCESS,
            data=serializer_detail(instance=instance_sr).data
        )
    
    def change_status(self, request, *args, **kwargs):
        serializer_detail = self.get_serializer_class_detail()

        instance = self.check_info()
        updated_data = self.get_context_updated()
        if not instance:
            return ResponseBuilder.build(
                code=ResponseCodes.INVALID_INPUT
            )
        if instance.is_active is True:
            instance.is_active = False
        else:
            instance.is_active = True
            
        instance.updated_by = updated_data.get('updated_by')
        instance.save(update_fields=['is_active', 'updated_by'])
        return ResponseBuilder.build(
            code=ResponseCodes.SUCCESS,
            data=serializer_detail(instance=instance).data
        )


class DestroyMixin(BaseMixin):
    def get_context_deleted(self):
        user_email = self.get_request_info_user()
        return {
            'deleted_at': timezone.now(),
            'deleted_by': user_email,
        }
    def destroy_many(self, request, *args, **kwargs):
        query_param = self.query_params()
        list_id_by_delete = query_param.getlist('id[]')
        if not list_id_by_delete:
            return ResponseBuilder.build(
                code=ResponseCodes.INVALID_INPUT,
            )
        try:
            with transaction.atomic(): 
                deleted_data = self.get_context_deleted()
                for obj_id in list_id_by_delete:
                    obj = self.check_info(lookup_value=obj_id)
                    if not obj:
                        raise
                    obj.is_deleted = True
                    obj.deleted_at = deleted_data.get('deleted_at')
                    obj.deleted_by = deleted_data.get('deleted_by')
                    obj.save(update_fields=['is_deleted', 'deleted_by', 'deleted_at'])
        except Exception:
            return ResponseBuilder.build(
                code=ResponseCodes.INVALID_INPUT,
            )
        return ResponseBuilder.build(
            code=ResponseCodes.SUCCESS,
        )
    
class DetailMixin(BaseMixin):
    def detail(self, request, *args, **kwargs):
        serializer_detail = self.get_serializer_class_detail()
        if not serializer_detail:
            return ResponseBuilder.build(
                code=ResponseCodes.SYSTEM_ERROR,
                errors="Serializer not found."
            )
        instance = self.check_info()
        if not instance:
            return ResponseBuilder.build(
                code=ResponseCodes.INVALID_INPUT
            )
        return ResponseBuilder.build(
            code=ResponseCodes.SUCCESS,
            data=serializer_detail(instance=instance).data
        )
