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
from apps.shared.response import ResponseFormat
from apps.shared.models import BaseModelCreated, BaseModelUpdated, BaseModelDeleted

class BaseMixin(GenericAPIView):
    serializer_class_list: serializers.Serializer
    serializer_class_create: serializers.Serializer
    serializer_class_detail: serializers.Serializer
    serializer_class_update: serializers.Serializer

    def get_serializer_class(self):
        if not self.serializer_class:
            if self.serializer_class_list:
                return self.serializer_class_list
        return self.serializer_class

    def get_serializer_class_list(self, *args, context: dict = None, **kwargs):
        if not context:
            context = self.get_serializer_context()
        func = getattr(self, 'serializer_class_list', None)
        if func and callable(func):
            return func(*args, context=context, **kwargs)  # pylint: disable=E1102
        raise ValueError('Serializer list attribute in view must be implement.')

    def get_serializer_class_create(self, *args, context: dict = None, **kwargs):
        if not context:
            context = self.get_serializer_context()
        func = getattr(self, 'serializer_class_create', None)
        if func and callable(func):
            return func(*args, context=context, **kwargs)  # pylint: disable=E1102
        raise ValueError('Serializer create attribute in view must be implement.')

    def get_serializer_class_detail(self, *args, context: dict = None, **kwargs):
        if not context:
            context = self.get_serializer_context()
        func = getattr(self, 'serializer_class_detail', None)
        if func and callable(func):
            return func(*args, context=context, **kwargs)  # pylint: disable=E1102
        raise ValueError('Serializer detail attribute in view must be implement.')

    def get_serializer_class_update(self, *args, context: dict = None, **kwargs):
        if not context:
            context = self.get_serializer_context()
        func = getattr(self, 'serializer_class_update', None)
        if func and callable(func):
            return func(*args, context=context, **kwargs)  # pylint: disable=E1102
        raise ValueError('Serializer update attribute in view must be implement.')

    def get_request_data(self) -> dict:
        return getattr(self.request, 'data', {})

    @property
    def is_dropdown(self):
        return self.request.headers.get('IS-DROPDOWN', '0') in ['1', 'true']

    @property
    def query_params(self):
        return getattr(self.request, 'query_params', {})

    class Meta:
        abstract = True


class ListMixin(BaseMixin):
    def get_serializer_context(self) -> dict:
        return {
            **super().get_serializer_context(),
            'is_dropdown': self.is_dropdown,
        }

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset().filter())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer_class_list(
                page, many=True, context=self.get_serializer_context()
            )
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer_class_list(
            queryset, many=True, context=self.get_serializer_context(),
        )
        return ResponseFormat.list(data=serializer.data)


class CreateMixin(BaseMixin):
    def get_create_data(self):
        return self.get_request_data()

    def create_save_context(self):
        context = {}
        model_cls = getattr(self.queryset, 'model', None)
        if model_cls:
            if issubclass(model_cls, BaseModelCreated):
                context['created_by_id'] = self.request.user.pk if self.request.user else None
            if issubclass(model_cls, BaseModelUpdated):
                context['updated_by_id'] = self.request.user.pk if self.request.user else None
        return context

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer_class_create(
            data=self.get_create_data(), context=self.get_serializer_context()
        )
        serializer.is_valid(raise_exception=True)
        instance = serializer.save(**self.create_save_context())
        return ResponseFormat.created(data=self.get_serializer_class_detail(instance=instance).data)


class RetrieveMixin(BaseMixin):
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance:
            ser = self.get_serializer_class_detail(
                instance=instance,
                context=self.get_serializer_context()
            )
            return ResponseFormat.retrieved(data=ser.data)
        return ResponseFormat.not_found()


class UpdateMixin(BaseMixin):
    def get_update_data(self):
        return self.get_request_data()

    def update_save_context(self):
        context = {}
        model_cls = getattr(self.queryset, 'model', None)
        if model_cls:
            if issubclass(model_cls, BaseModelUpdated):
                context['updated_by_id'] = self.request.user.pk if self.request.user else None
        return context

    def update(self, request, *args, partial: bool = False, **kwargs):
        instance = self.get_object()
        if instance:
            serializer = self.get_serializer_class_update(
                instance=instance, data=self.get_update_data(), partial=partial,
                context=self.get_serializer_context(),
            )
            serializer.is_valid(raise_exception=True)
            instance_sr = serializer.save(**self.update_save_context())
            return ResponseFormat.updated(data=self.get_serializer_class_detail(instance=instance_sr).data)
        return ResponseFormat.not_found()


class DestroyMixin(BaseMixin):
    def perform_delete(self, obj, is_purge=False):
        if is_purge is False:
            if issubclass(obj.__class__, BaseModelDeleted):
                return obj.delete(is_purge=is_purge, deleted_by_id=self.request.user.pk if self.request.user else None)
        return obj.delete(is_purge=is_purge)

    @classmethod
    def delete_is_purge(cls) -> bool:
        """
        Cho phép destroy vĩnh viễn dữ liệu, False: sử dụng soft-delete.
        """
        return False

    def destroy(self, request, *args, **kwargs):
        is_purge = self.delete_is_purge()
        instance = self.get_object()
        if instance:
            self.perform_delete(instance, is_purge=is_purge)
            return ResponseFormat.deleted()
        return ResponseFormat.not_found()

    def destroy_many(self, request, *args, **kwargs):
        is_purge = self.delete_is_purge()
        ids = request.query_params.getlist('ids[]', None)
        if ids:
            try:
                queryset = self.get_queryset().filter(pk__in=ids)
            except (ValueError, TypeError, self.queryset.model.DoesNotExist):
                ...
            else:
                for obj in queryset:
                    self.perform_delete(obj, is_purge=is_purge)
                return ResponseFormat.deleted()
        return ResponseFormat.not_found()

