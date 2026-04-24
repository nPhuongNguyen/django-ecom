

from ..models.role_permission import RolePermission


class RolePermissionRepository:
    _role_permission_model = RolePermission

    def list_permission_by_list_role(self, list_role, is_active):
        return (self._role_permission_model.objects
                .filter(
                    role_id__in=list_role,
                    is_active=is_active,
                    permission__is_active=True,
                    role__is_active=True,
                )
                .values_list('permission__code', flat=True)
                .distinct() # User có thể có nhiều role, nên cần distinct để tránh trùng lặp permission
            )