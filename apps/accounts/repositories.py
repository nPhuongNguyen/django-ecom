
from .models.users import Users

class AccountsRepository:
    _instance = None
    _initialized = False
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self.model_user = Users
            self._initialized = True
    pass