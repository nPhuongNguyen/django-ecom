
import uuid
from django.db import models
from apps.shared.models import BaseModelActive, BaseModelCreated, BaseModelDeleted, BaseModelInt, BaseModelUpdated
from apps.shared.views_api.generate import generate_code
class Order(BaseModelInt, BaseModelActive, BaseModelCreated, BaseModelUpdated, BaseModelDeleted):
    code = models.CharField(max_length=100, unique=True, default=generate_code('ORDER'))
    status = models.CharField(max_length=50, choices=[
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ], default='pending')
    note = models.TextField(blank=True, null=True)
    total_amount  = models.IntegerField(default=0)
    subtotal_amount = models.IntegerField(default=0)
    discount_amount = models.IntegerField(default=0)
    payment_id = models.IntegerField(default=0)
    class Meta:
        db_table = 'sales_order'