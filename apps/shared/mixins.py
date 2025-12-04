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
from apps.shared.models import BaseModelCreated, BaseModelUpdated, BaseModelDeleted
from apps.shared.response import ResponseBuilder, ResponseCodes
from django.db import transaction
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

    def create(self, request, *args, **kwargs):
        serializer_create = self.get_serializer_class_create()
        serializer_detail = self.get_serializer_class_detail()

        if not serializer_create or not serializer_detail:
            return ResponseBuilder.build(
                code=ResponseCodes.SYSTEM_ERROR,
                errors="Serializer not found."
            )

        serializer = serializer_create(data=self.get_create_data())
        if not serializer.is_valid():
            return ResponseBuilder.build(
                code=ResponseCodes.INVALID_INPUT,
                errors=serializer.errors
            )

        instance = serializer.save()
        return ResponseBuilder.build(
            code=ResponseCodes.SUCCESS,
            data=serializer_detail(instance=instance).data
        )

class UpdateMixin(BaseMixin):
    def get_update_data(self):
        return self.get_request_data()

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
        instance_sr = serializer.save()
        return ResponseBuilder.build(
            code=ResponseCodes.SUCCESS,
            data=serializer_detail(instance=instance_sr).data
        )


class DestroyMixin(BaseMixin):
    def destroy_many(self, request, *args, **kwargs):
        query_param = self.query_params()
        list_id_by_delete = query_param.getlist('id[]')
        if not list_id_by_delete:
            return ResponseBuilder.build(
                code=ResponseCodes.INVALID_INPUT,
            )
        try:
            with transaction.atomic(): 
                for id in list_id_by_delete:
                    obj = self.check_info(lookup_value=id)
                    if not obj:
                        raise 
                    obj.is_deleted = True
                    obj.save(update_fields=['is_deleted'])
        except Exception:
            return ResponseBuilder.build(
                code=ResponseCodes.INVALID_INPUT,
            )
        return ResponseBuilder.build(
            code=ResponseCodes.SUCCESS,
        )
