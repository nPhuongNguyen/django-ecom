from django.db import models
from apps.shared.models import BaseModelActive, BaseModelCreated, BaseModelDeleted, BaseModelInt, BaseModelUpdated
class Role(BaseModelInt, BaseModelActive, BaseModelCreated, BaseModelUpdated, BaseModelDeleted):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100)

    class Meta:
        db_table = 'core_roles'
