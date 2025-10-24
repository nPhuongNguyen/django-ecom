from django.db import models
from apps.shared.models import BaseModelActive, BaseModelCreated, BaseModelDeleted, BaseModelInt, BaseModelUpdated

# Create your models here.
class Users(BaseModelInt, BaseModelActive, BaseModelCreated, BaseModelUpdated, BaseModelDeleted):
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = 'core_users'