

from ..models.user import User

class UserRepository:
    _user_model = User

    def get_user_by_email(self, email, is_active):
        return self._user_model.objects.filter(email=email, is_active=is_active).first()