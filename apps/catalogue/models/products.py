from django.db import models
from apps.catalogue.models.categories import Category
from apps.catalogue.models.collection import Collection
from apps.shared.models import BaseModelActive, BaseModelCreated, BaseModelDeleted, BaseModelInt, BaseModelUpdated
# Create your models here.

class Product(BaseModelInt, BaseModelActive, BaseModelCreated, BaseModelUpdated, BaseModelDeleted):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    description = models.TextField(blank=True)
    img = models.CharField(max_length=255, blank=True)
    category = models.ForeignKey(Category, db_column='category_id' , on_delete=models.RESTRICT, null=True)

    class Meta:
        db_table = 'catalogue_products'

class ProductVariant(BaseModelInt, BaseModelActive, BaseModelCreated, BaseModelUpdated, BaseModelDeleted):
    product = models.ForeignKey(Product, db_column= 'product_id', on_delete=models.RESTRICT, related_name='variants')
    name = models.CharField(max_length=100)
    img = models.CharField(max_length=255, blank=True)
    sku = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock_qty = models.IntegerField(default=0)

    class Meta:
        db_table = 'catalogue_product_variants'

class Attribute(BaseModelInt, BaseModelActive, BaseModelCreated, BaseModelUpdated, BaseModelDeleted):
    name = models.CharField(max_length=100)
    class Meta:
        db_table = 'catalogue_attribute'

class AttributeValue(BaseModelInt, BaseModelActive, BaseModelCreated, BaseModelUpdated, BaseModelDeleted):
    name = models.CharField(max_length=50)
   
    class Meta:
        db_table = 'catalogue_attribute_value'

class M2MAttribute(BaseModelInt, BaseModelActive, BaseModelCreated, BaseModelUpdated, BaseModelDeleted):
    attribute = models.ForeignKey(Attribute, db_column='attribute_id', on_delete=models.RESTRICT)
    attribute_value = models.ForeignKey(AttributeValue, db_column='attribute_value_id', on_delete=models.RESTRICT)
    class Meta:
        db_table = 'catalogue_m2m_attribute'
        unique_together = ('attribute_id','attribute_value_id')

class M2MProductVarianAttribute(BaseModelInt, BaseModelActive, BaseModelCreated, BaseModelUpdated, BaseModelDeleted):
    product_variant = models.ForeignKey(ProductVariant, db_column='product_variant_id',on_delete=models.RESTRICT)
    m2m_attribute = models.ForeignKey(Attribute, db_column='m2m_attribute_id',on_delete=models.RESTRICT)

    class Meta:
        db_table = 'catalogue_m2m_product_variant_attribute'
        unique_together = ('product_variant_id', 'm2m_attribute_id')