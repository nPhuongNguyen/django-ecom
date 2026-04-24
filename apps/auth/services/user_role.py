from ..repositories.user_role import UserRoleRepository
from apps.logging import logging_log as lg

class UserRoleService:
    def __init__(self):
        self.user_role_repository = UserRoleRepository()

    def get_list_role_by_user_id(self, user_id, is_active=True):
        try:
            return self.user_role_repository.get_list_role_by_user_id(user_id, is_active)
        except Exception as e:
            lg.log_error("[ERROR] get_list_role_by_user_id", user_id=user_id, is_active=is_active, error=str(e))
            return []
        
    def get_role_code_by_user_id(self, user_id, is_active=True):
        try:
            return self.user_role_repository.get_role_code_by_user_id(user_id,is_active)
        except Exception as e:
            lg.log_error("[ERROR] get_role_code_by_user_id", user_id=user_id, is_active=is_active, error=str(e))
            return []