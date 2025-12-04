__all__ = [
    'BaseModel',
    'BaseModelInt',
    'BaseModelStatus',
    'BaseModelActive',
    'BaseModelCreated',
    'BaseModelUpdated',
    'BaseModelDeleted',
]

from django.conf import settings
from django.db import models
from django.utils import timezone
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
    is_active = models.BooleanField(default=True, db_comment='Trạng thái kích hoạt')

    class Meta:
        abstract = True


class BaseModelCreated(BaseModel):
    created_at = models.DateTimeField(auto_now_add=True, db_comment='Ngày tạo')
    created_by = models.ForeignKey(
        'auths.Users', on_delete=models.RESTRICT, # pylint: disable=E5141
        db_column='created_by_id',
        db_comment='Người tạo',
        related_name='%(app_label)s_%(class)s_created_by',
        null=True,  # temp for system master | need fill default '1' when init data
    )

    class Meta:
        abstract = True


class BaseModelUpdated(BaseModel):
    updated_at = models.DateTimeField(auto_now=True, db_comment='Ngày cập nhật cuối')
    updated_by = models.ForeignKey(
        'auths.Users', on_delete=models.RESTRICT, # pylint: disable=E5141
        db_column='updated_by_id',
        db_comment='Người cập nhật cuối',
        related_name='%(app_label)s_%(class)s_updated_by',
        null=True,  # temp for system master | need fill default '1' when init data
    )

    class Meta:
        abstract = True


class BaseModelDeleted(BaseModel):
    is_deleted = models.BooleanField(default=False, db_comment='Trạng thái đã xoá')
    deleted_at = models.DateTimeField(null=True, db_comment='Ngày đã xoá')
    deleted_by = models.ForeignKey(
        'auths.Users', on_delete=models.RESTRICT, # pylint: disable=E5141
        db_column='deleted_by_id',
        db_comment='Người đã xoá',
        related_name='%(app_label)s_%(class)s_deleted_by',
    )

    def delete(self, *args, is_purge: bool = False, deleted_by_id: int = None, **kwargs):
        if is_purge is True:
            return super().delete(*args, **kwargs)
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.deleted_by_id = deleted_by_id  # pylint: disable=W0201
        return super().save()

    class Meta:
        abstract = True
