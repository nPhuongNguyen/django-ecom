from django.db import models
from ...shared.models import BaseModelActive, BaseModelCreated, BaseModelDeleted, BaseModelInt, BaseModelUpdated


class TemplateEmail(BaseModelInt, BaseModelActive, BaseModelCreated, BaseModelUpdated, BaseModelDeleted):
    format = models.TextField()
    code = models.CharField(max_length=100, unique=True)
    class Meta:
        db_table = 'email_template'