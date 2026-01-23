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
from apps.logging import logging_log as lg
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
    
    def perform_create(self, serializer, **kwargs):
        if kwargs:
            return serializer.save(**kwargs)
        return serializer.save()


    def query_params(self):
        return getattr(self.request, 'query_params', {})

    class Meta:
        abstract = True


class ListMixin(BaseMixin):
    def list(self, request, *args, **kwargs):
        query_params = dict(request.query_params)
        lg.log_info(
            message="[LIST][CALL]",
            input={
                "query_params": query_params
            }
        )
        serializer_class = self.get_serializer_class_list()
        if not serializer_class:
            lg.log_info(
                message="[LIST][CALL]",
                input={
                    "query_params": query_params
                }
            )

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
            lg.log_info(
                message="[LIST][SUCCESS][PAGINATED]",
                input={
                    "query_params": query_params
                },
                output={
                    "data": serializer.data
                }
            )
            return self.get_paginated_response(serializer.data)

        serializer = serializer_class(
            queryset, many=True
        )
        lg.log_info(
            message="[LIST][SUCCESS]",
            input={
                "query_params": query_params
            },
            output={
                "data": serializer.data
            }
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
        input_data = self.get_create_data()

        lg.log_info(
            message="[CREATE][CALL]",
            input=input_data
        )
        serializer_create = self.get_serializer_class_create()
        serializer_detail = self.get_serializer_class_detail()


        if not serializer_create or not serializer_detail:
            lg.log_error(
                message="[CREATE][SERIALIZER_NOT_FOUND]",
                input=input_data,
                serializer_create=str(serializer_create),
                serializer_detail=str(serializer_detail)
            )
            return ResponseBuilder.build(
                code=ResponseCodes.SYSTEM_ERROR,
                errors="Serializer not found."
            )

        serializer = serializer_create(data=input_data)
        if not serializer.is_valid():
            lg.log_error(
                message="[CREATE][SERIALIZER_NOT_FOUND]",
                input=input_data,
                serializer_create=str(serializer_create),
                serializer_detail=str(serializer_detail)
            )
            return ResponseBuilder.build(
                code=ResponseCodes.INVALID_INPUT,
                errors=serializer.errors
            )
        
        # instance = serializer.save(**self.get_context_created())
        instance = self.perform_create(serializer, **self.get_context_created())
        output_data = serializer_detail(instance=instance).data
        lg.log_info(
            message="[CREATE][SUCCESS]",
            input=input_data,
            output=output_data
        )
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

    def update(self, request, partial=False, *args, **kwargs):
        input_data = self.get_update_data()
        object_id = self.kwargs.get("pk")
        input_data={
            "id": object_id,
            "data": input_data,
            "partial": partial
        }
        lg.log_info(
            message="[UPDATE][CALL]",
            input=input_data
        )
        serializer_update = self.get_serializer_class_update()
        serializer_detail = self.get_serializer_class_detail()
        if not serializer_update or not serializer_detail:
            lg.log_error(
                message="[UPDATE][SERIALIZER_NOT_FOUND]",
                input=input_data,
                serializer_update=str(serializer_update),
                serializer_detail=str(serializer_detail)
            )
            return ResponseBuilder.build(
                code=ResponseCodes.SYSTEM_ERROR,
                errors="Serializer not found."
            )
        
        instance = self.check_info()
        if not instance:
            lg.log_error(
                message="[UPDATE][INSTANCE_NOT_FOUND]",
                input=input_data
            )
            return ResponseBuilder.build(
                code=ResponseCodes.INVALID_INPUT
            )
        serializer = serializer_update(
            instance=instance, data=self.get_update_data(), partial=partial
        )
        if not serializer.is_valid():
            lg.log_error(
                message="[UPDATE][VALIDATION_FAILED]",
                input=input_data,
                errors=serializer.errors
            )
            return ResponseBuilder.build(
                code=ResponseCodes.INVALID_INPUT,
                errors=serializer.errors
            )
        instance_sr = serializer.save(**self.get_context_updated())
        output_data = serializer_detail(instance=instance_sr).data
        lg.log_info(
            message="[UPDATE][SUCCESS]",
            input=input_data,
            output=output_data
        )
        return ResponseBuilder.build(
            code=ResponseCodes.SUCCESS,
            data=output_data
        )
    
    def change_status(self, request, *args, **kwargs):
        serializer_detail = self.get_serializer_class_detail()
        object_id = self.kwargs.get("pk")
        updated_data = self.get_context_updated()

        input_data = {
            "id": object_id,
            "updated_by": updated_data.get("updated_by")
        }

        lg.log_info(
            message="[CHANGE_STATUS][CALL]",
            input=input_data
        )

        instance = self.check_info()
        updated_data = self.get_context_updated()
        if not instance:
            lg.log_error(
                message="[CHANGE_STATUS][INSTANCE_NOT_FOUND]",
                input=input_data
            )
            return ResponseBuilder.build(
                code=ResponseCodes.INVALID_INPUT
            )
        instance.is_active = not instance.is_active
            
        instance.updated_by = updated_data.get('updated_by')
        instance.save(update_fields=['is_active', 'updated_by'])
        output_data = serializer_detail(instance=instance).data
        lg.log_info(
            message="[CHANGE_STATUS][SUCCESS]",
            input=input_data,
            output=output_data
        )
        return ResponseBuilder.build(
            code=ResponseCodes.SUCCESS,
            data=output_data
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
        input_data = {
            "id[]": list_id_by_delete
        }
        lg.log_info(
            message="[DESTROY_MANY][CALL]",
            input=input_data
        )
        if not list_id_by_delete:
            lg.log_error(
                message="[DESTROY_MANY][EMPTY_IDS]",
                input=input_data
            )
            return ResponseBuilder.build(
                code=ResponseCodes.INVALID_INPUT,
            )
        try:
            with transaction.atomic(): 
                deleted_data = self.get_context_deleted()
                deleted_ids = []
                for obj_id in list_id_by_delete:
                    obj = self.check_info(lookup_value=obj_id)
                    if not obj:
                        lg.log_error(
                            message="[DESTROY_MANY][OBJECT_NOT_FOUND]",
                            input={"id": obj_id}
                        )
                        raise ValueError(f"Object not found: {obj_id}")
                    obj.is_deleted = True
                    obj.deleted_at = deleted_data.get('deleted_at')
                    obj.deleted_by = deleted_data.get('deleted_by')
                    obj.save(update_fields=['is_deleted', 'deleted_by', 'deleted_at'])
                    deleted_ids.append(obj_id)
        except Exception as err:
            lg.log_error(
                message="[DESTROY_MANY][FAILED]",
                input=input_data,
                error=str(err)
            )
            return ResponseBuilder.build(
                code=ResponseCodes.INVALID_INPUT,
                errors=str(err)
            )
        lg.log_info(
            message="[DESTROY_MANY][SUCCESS]",
            input=input_data,
            output={
                "deleted_ids": deleted_ids,
                "deleted_by": deleted_data.get("deleted_by"),
                "deleted_at": deleted_data.get("deleted_at"),
            }
        )
        return ResponseBuilder.build(
            code=ResponseCodes.SUCCESS,
        )
    
class DetailMixin(BaseMixin):
    def detail(self, request, *args, **kwargs):
        object_id = self.kwargs.get("pk")
        input_data = {
            "id": object_id
        }

        lg.log_info(
            message="[DETAIL][CALL]",
            input=input_data
        )
        serializer_detail = self.get_serializer_class_detail()
        if not serializer_detail:
            lg.log_error(
                message="[DETAIL][SERIALIZER_NOT_FOUND]",
                input=input_data
            )
            return ResponseBuilder.build(
                code=ResponseCodes.SYSTEM_ERROR,
                errors="Serializer not found."
            )
        instance = self.check_info()
        if not instance:
            lg.log_error(
                message="[DETAIL][INSTANCE_NOT_FOUND]",
                input=input_data
            )
            return ResponseBuilder.build(
                code=ResponseCodes.INVALID_INPUT
            )
        output_data = serializer_detail(instance=instance).data
        lg.log_info(
            message="[DETAIL][SUCCESS]",
            input=input_data,
            output=output_data
        )
        return ResponseBuilder.build(
            code=ResponseCodes.SUCCESS,
            data=output_data
        )
