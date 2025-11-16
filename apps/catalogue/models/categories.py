from django.db import models
from apps.shared.models import BaseModelActive, BaseModelCreated, BaseModelDeleted, BaseModelInt, BaseModelUpdated
class Category(BaseModelInt, BaseModelActive, BaseModelCreated, BaseModelUpdated, BaseModelDeleted):
    name = models.CharField(max_length=100)
    sku = models.CharField(max_length=100, unique=True)
    class Meta:
        db_table = 'catalogue_product_categories'
