from django.db import models
from apps.catalogue.models.categories import Category
from apps.catalogue.models.collection import Collection
from apps.shared.models import BaseModelActive, BaseModelCreated, BaseModelDeleted, BaseModelInt, BaseModelUpdated
# Create your models here.

class Product(BaseModelInt, BaseModelActive, BaseModelCreated, BaseModelUpdated, BaseModelDeleted):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=150, unique=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    img = models.CharField(max_length=255, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    category = models.ForeignKey(Category, db_column='category_id' , on_delete=models.RESTRICT, blank=True, null=True)

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, db_column= 'product_id', on_delete=models.RESTRICT)
    name = models.CharField(max_length=255, null=True)
    img = models.CharField(max_length=200, null=True, blank=True)
    sku = models.CharField(max_length=50, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock_qty = models.IntegerField(default=0)
    is_deleted = models.BooleanField(default=False)

class Option(models.Model):
    name = models.CharField(max_length=50)
    is_deleted = models.BooleanField(default=False)


class OptionValue(models.Model):
    option = models.ForeignKey(Option, db_column= 'option_id',on_delete=models.RESTRICT)
    value = models.CharField(max_length=50)

class VariantOptionValue(models.Model):
    variant = models.ForeignKey(ProductVariant, db_column='variant_id', on_delete=models.RESTRICT)
    option_value = models.ForeignKey(OptionValue, on_delete=models.RESTRICT)
    class Meta:
        unique_together = ('variant', 'option_value')
