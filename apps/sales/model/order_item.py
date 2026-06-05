from django.db import models
from apps.catalogue.models.products import ProductVariant
from apps.sales.model.order import Order
from apps.shared.models import BaseModel, BaseModelActive, BaseModelCreated, BaseModelDeleted, BaseModelInt, BaseModelUpdated

class OrderItem(BaseModelInt, BaseModelActive, BaseModelCreated, BaseModelUpdated, BaseModelDeleted):
    order = models.ForeignKey(Order, db_column='order_id', on_delete=models.RESTRICT)
    product_variant_id = models.ForeignKey(ProductVariant, db_column='product_variant_id', on_delete=models.RESTRICT)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField(default=0)
    total_price = models.IntegerField(default=0)

    class Meta:
        db_table = 'sales_order_item'
        
class CarItem(BaseModel):
    user_id = models.IntegerField()
    product_variant = models.ForeignKey(ProductVariant, db_column='product_variant_id', on_delete=models.RESTRICT)
    quantity = models.IntegerField(default=1)
    class Meta:
        abstract = True