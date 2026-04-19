from django.db import models
from .role import Role
from .permission import Permission
from apps.shared.models import BaseModelActive, BaseModelCreated, BaseModelDeleted, BaseModelInt, BaseModelUpdated

class RolePermission(BaseModelInt, BaseModelActive, BaseModelCreated, BaseModelUpdated, BaseModelDeleted):
    role = models.ForeignKey(Role, on_delete=models.RESTRICT)
    permission = models.ForeignKey(Permission, on_delete=models.RESTRICT)

    class Meta:
        db_table = 'core_m2m_role_permission'