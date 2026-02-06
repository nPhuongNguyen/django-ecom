__all__ = [
    'BaseModel',
    'BaseModelInt',
    'BaseModelStatus',
    'BaseModelActive',
    'BaseModelCreated',
    'BaseModelUpdated',
    'BaseModelDeleted',
]

from django.db import models
from .model_manager import BaseManager


class BaseModel(models.Model):
    objects = BaseManager()
    class Meta:
        abstract = True
        ordering = ('-created_at',)
        default_permissions = ()


class BaseModelInt(BaseModel):
    id = models.AutoField(primary_key=True, editable=False)

    class Meta:
        abstract = True


class BaseModelActive(BaseModel):
    is_active = models.BooleanField(default=False, db_comment='Trạng thái kích hoạt')

    class Meta:
        abstract = True


class BaseModelCreated(BaseModel):
    created_at = models.DateTimeField(auto_now_add=True, db_comment='Ngày tạo')
    created_by = models.CharField(max_length=200, blank=True)

    class Meta:
        abstract = True


class BaseModelUpdated(BaseModel):
    updated_at = models.DateTimeField(auto_now=True, db_comment='Ngày cập nhật cuối')
    updated_by = models.CharField(max_length=200, blank=True)

    class Meta:
        abstract = True


class BaseModelDeleted(BaseModel):
    is_deleted = models.BooleanField(default=False, db_comment='Trạng thái đã xoá')
    deleted_at = models.DateTimeField(blank=True, db_comment='Ngày đã xoá')
    deleted_by = models.CharField(max_length=200, blank=True)
    class Meta:
        abstract = True
