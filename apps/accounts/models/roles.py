from django.db import models
from .permissions import Permissions
from apps.shared.models import BaseModelActive, BaseModelCreated, BaseModelDeleted, BaseModelInt, BaseModelUpdated
class Roles(BaseModelInt, BaseModelActive, BaseModelCreated, BaseModelUpdated, BaseModelDeleted):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100)

    class Meta:
        db_table = 'core_roles'

class RolePermissions(BaseModelInt, BaseModelActive, BaseModelCreated, BaseModelUpdated, BaseModelDeleted):
    role = models.ForeignKey(Roles, on_delete=models.RESTRICT)
    permission = models.ForeignKey(Permissions, on_delete=models.RESTRICT)

    class Meta:
        db_table = 'core_m2m_role_permission'