
from .repositories import AccountsRepository

class AccountsService:
    _instance = None
    _initialized = False
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self.repository = AccountsRepository()
            self._initialized = True
    pass