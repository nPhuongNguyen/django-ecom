

from ..models.user_role import UserRole


class UserRoleRepository:
    _user_role_model = UserRole
    def get_list_role_by_user_id(self, user_id, is_active):
        return self._user_role_model.objects.filter(user_id=user_id, is_active=is_active).values_list('role_id', flat=True)
    
    def get_role_code_by_user_id(self, user_id, is_active):
        return (self._user_role_model.objects.filter(
                user_id=user_id,
                is_active=is_active,
                role__is_active=True
            )
            .values_list('role__code', flat=True)
        )