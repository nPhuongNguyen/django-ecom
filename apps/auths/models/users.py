from django.db import models
from apps.shared.models import BaseModelActive, BaseModelCreated, BaseModelDeleted, BaseModelInt, BaseModelUpdated

# Create your models here.
class Users(BaseModelInt, BaseModelActive, BaseModelCreated, BaseModelUpdated, BaseModelDeleted):
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    is_super = models.BooleanField(default=0)
    last_login = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'core_users'