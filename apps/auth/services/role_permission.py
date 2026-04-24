

from ..repositories.role_permission import RolePermissionRepository
from apps.logging import logging_log as lg

class RolePermissionService:
    def __init__(self):
        self.role_permission_model = RolePermissionRepository()

    def list_permission_by_list_role(self, list_role, is_active=True):
        try:
            return self.role_permission_model.list_permission_by_list_role(list_role, is_active)
        except Exception as e:
            lg.log_error("[ERROR] list_permission_by_list_role", list_role=list_role,is_active=is_active,error=str(e))
            return []