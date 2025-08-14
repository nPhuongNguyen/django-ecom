from django.db import models
class Category(models.Model):
    name = models.CharField(max_length=100)
    sku = models.CharField(max_length=150, unique=True)
    is_deleted = models.BooleanField(default=False)