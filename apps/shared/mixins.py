__all__ = [
    'BaseMixin',
    'ListMixin',
    'CreateMixin',
    'RetrieveMixin',
    'UpdateMixin',
    'DestroyMixin',
]
from rest_framework import serializers
from rest_framework.generics import GenericAPIView
from apps.logging import logging_log as lg
from .decorator.decorator import track_execution
from apps.shared.response import ResponseBuilder, ResponseCodes
from django.db import transaction
from django.utils import timezone
class BaseMixin(GenericAPIView):
    serializer_class_list: serializers.Serializer
    serializer_class_create: serializers.Serializer
    serializer_class_detail: serializers.Serializer
    serializer_class_update: serializers.Serializer
    serializer_class_destroy: serializers.Serializer
    serializer_class_change_status : serializers.Serializer

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
    
    def get_serializer_class_destroy(self):
        serializer_cls =  getattr(self, 'serializer_class_destroy', None)
        if serializer_cls is None:
            return None
        return serializer_cls
    
    def get_serializer_class_change_status(self):
        serializer_cls =  getattr(self, 'serializer_class_change_status', None)
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
    
    def perform_create(self, serializer, **kwargs):
        if kwargs:
            return serializer.save(**kwargs)
        return serializer.save()
    
    def perform_update(self, instance, **kwargs):
        if kwargs:
            return instance.save(**kwargs)
        return instance.save()

    def query_params(self):
        return getattr(self.request, 'query_params', {})

    class Meta:
        abstract = True


class ListMixin(BaseMixin):
    @track_execution("LIST")
    def list(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class_list()
        if not serializer_class:
            return ResponseBuilder.build(
                code=ResponseCodes.SYSTEM_ERROR,
                errors="Serializer not found."
            )
        queryset = self.filter_queryset(self.get_queryset().filter())
        page = self.paginate_queryset(queryset)
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
    @track_execution("CREATE")
    def create(self, request, *args, **kwargs):
        input_data = self.get_create_data()
        serializer_create = self.get_serializer_class_create()
        serializer_detail = self.get_serializer_class_detail()
        if not serializer_create or not serializer_detail:
            return ResponseBuilder.build(
                code=ResponseCodes.SYSTEM_ERROR,
                errors="Serializer not found."
            )
        serializer = serializer_create(data=input_data)
        if not serializer.is_valid():
            return ResponseBuilder.build(
                code=ResponseCodes.INVALID_INPUT,
                errors=serializer.errors
            )
        instance = self.perform_create(serializer, **self.get_context_created())
        instance.refresh_from_db()
        output_data = serializer_detail(instance=instance).data
        return ResponseBuilder.build(
            code=ResponseCodes.SUCCESS,
            data=output_data
        )

class UpdateMixin(BaseMixin):
    def get_update_data(self):
        return self.get_request_data()
    
    def get_context_updated(self):
        user_email = self.get_request_info_user()
        return {
            'updated_by': user_email,
        }
    @track_execution("UPDATE")
    def update(self, request, partial=False, *args, **kwargs):
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
            instance=instance, data=self.get_update_data(), partial=partial
        )
        if not serializer.is_valid():
            return ResponseBuilder.build(
                code=ResponseCodes.INVALID_INPUT,
                errors=serializer.errors
            )
        instance_sr = self.perform_update(serializer, **self.get_context_updated())
        output_data = serializer_detail(instance=instance_sr).data
        return ResponseBuilder.build(
            code=ResponseCodes.SUCCESS,
            data=output_data
        )
    
    @track_execution("CHANGE_STATUS")
    def change_status(self, request, *args, **kwargs):
        serializer_detail = self.get_serializer_class_detail()
        serializer_change_status = self.get_serializer_class_change_status()
        if not serializer_change_status or not serializer_detail:
            return ResponseBuilder.build(
                code=ResponseCodes.SYSTEM_ERROR,
                errors="Serializer not found."
            )
        instance = self.check_info()
        if not instance:
            return ResponseBuilder.build(
                code=ResponseCodes.INVALID_INPUT
            )
        serializer = serializer_change_status(instance=instance, data={
            'is_active': not instance.is_active
        })
        if not serializer.is_valid():
            return ResponseBuilder.build(
                code=ResponseCodes.INVALID_INPUT,
                errors=serializer.errors
            )
        instance_sr = self.perform_update(serializer, **self.get_context_updated())
        instance_sr.refresh_from_db()
        output_data = serializer_detail(instance=instance_sr).data
        return ResponseBuilder.build(
            code=ResponseCodes.SUCCESS,
            data=output_data
        )
        
class DestroyMixin(BaseMixin):
    def get_context_deleted(self):
        user_email = self.get_request_info_user()
        return {
            'is_deleted': True,
            'deleted_at': timezone.now(),
            'deleted_by': user_email,
        }
    @track_execution("DESTROY")
    def destroy_many(self, request, *args, **kwargs):
        query_param = self.query_params()
        list_id_by_delete = query_param.getlist('id[]')
        if not list_id_by_delete:
            return ResponseBuilder.build(
                code=ResponseCodes.INVALID_INPUT,
            )
        serializer_destroy = self.get_serializer_class_destroy()
        if not serializer_destroy:
            return ResponseBuilder.build(
                code=ResponseCodes.SYSTEM_ERROR,
                errors="Serializer not found."
            )
        try:
            with transaction.atomic(): 
                for obj_id in list_id_by_delete:
                    obj = self.check_info(lookup_value=obj_id)
                    if not obj:
                        raise serializers.ValidationError(f"Không tìm thấy bản ghi với ID: {obj_id}")
                    context_data = self.get_context_deleted()
                    serializer = serializer_destroy(instance=obj, data=context_data)
                    serializer.is_valid(raise_exception=True)
                    self.perform_update(serializer)
        except serializers.ValidationError as e:
            return ResponseBuilder.build(
                code=ResponseCodes.INVALID_INPUT,
                errors=e.detail
            )
        return ResponseBuilder.build(
            code=ResponseCodes.SUCCESS,
        )
    
class DetailMixin(BaseMixin):
    @track_execution("DETAIL")
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
        output_data = serializer_detail(instance=instance).data
        return ResponseBuilder.build(
            code=ResponseCodes.SUCCESS,
            data=output_data
        )
