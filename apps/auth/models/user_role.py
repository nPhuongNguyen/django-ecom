from django.db import models

from ...accounts.models.user import User

from .role import Role
from ...shared.models import BaseModelActive, BaseModelCreated, BaseModelDeleted, BaseModelInt, BaseModelUpdated
class UserRole(BaseModelInt, BaseModelActive, BaseModelCreated, BaseModelUpdated, BaseModelDeleted):
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    role = models.ForeignKey(Role, on_delete=models.RESTRICT)

    class Meta:
        db_table = 'core_m2m_user_role'