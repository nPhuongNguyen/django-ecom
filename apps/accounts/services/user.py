

from ..repositories.user import UserRepository
from apps.logging import logging_log as lg

class UserService:
    def __init__(self):
        self._user_repository = UserRepository()

    def get_user_by_email(self, email, is_active=True):
        try:
            return self._user_repository.get_user_by_email(email, is_active)
        except Exception as e:
            lg.log_error(
                "[ERROR] get_user_by_email",
                email=email,
                error=str(e)
            )
            return None
        