from django.db import models
from apps.catalogue.models.categories import Category
from apps.catalogue.models.collection import Collection
from apps.shared.models import BaseModelActive, BaseModelCreated, BaseModelDeleted, BaseModelInt, BaseModelUpdated
# Create your models here.

class Product(BaseModelInt, BaseModelActive, BaseModelCreated, BaseModelUpdated, BaseModelDeleted):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    img = models.CharField(max_length=255, blank=True)
    category = models.ForeignKey(Category, db_column='category_id' , on_delete=models.RESTRICT, null=True)

    class Meta:
        db_table = 'catalogue_product'

class ProductVariant(BaseModelInt, BaseModelActive, BaseModelCreated, BaseModelUpdated, BaseModelDeleted):
    product = models.ForeignKey(Product, db_column= 'product_id', on_delete=models.RESTRICT, related_name='variants')
    name = models.CharField(max_length=100)
    img = models.CharField(max_length=255, blank=True)
    sku = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    stock_qty = models.IntegerField(default=0)

    class Meta:
        db_table = 'catalogue_product_variant'

class Attribute(BaseModelInt, BaseModelActive, BaseModelCreated, BaseModelUpdated, BaseModelDeleted):
    name = models.CharField(max_length=100)
    class Meta:
        db_table = 'catalogue_attribute'
        
class AttributeValue(BaseModelInt, BaseModelActive, BaseModelCreated, BaseModelUpdated, BaseModelDeleted):
    name = models.CharField(max_length=50)
    attribute = models.ForeignKey(Attribute, db_column= 'attribute_id', on_delete=models.RESTRICT,)
    class Meta:
        db_table = 'catalogue_attribute_value'
        
class M2MProductAttribute(BaseModelInt, BaseModelActive, BaseModelCreated, BaseModelUpdated, BaseModelDeleted):
    product = models.ForeignKey(Product, db_column= 'product_id', on_delete=models.RESTRICT)
    attribute = models.ForeignKey(Attribute, db_column= 'attribute_id', on_delete=models.RESTRICT,)
    
    class Meta:
        db_table = 'catalogue_m2m_product_attribute'
        unique_together = ('product', 'attribute')

class M2MProductVarianAttribute(BaseModelInt, BaseModelActive, BaseModelCreated, BaseModelUpdated, BaseModelDeleted):
    product_variant = models.ForeignKey(ProductVariant, db_column='product_variant_id',on_delete=models.RESTRICT)
    attribute_value = models.ForeignKey(AttributeValue, db_column='attribute_value_id',on_delete=models.RESTRICT)

    class Meta:
        db_table = 'catalogue_m2m_product_variant_attribute_value'
        unique_together = ('product_variant', 'attribute_value')