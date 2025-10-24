
from django.db import models
from django.utils.text import slugify

from apps.catalogue.models.categories import Category
from apps.catalogue.models.collection import Collection
from apps.catalogue.models.products import Product
class Promotion(models.Model):
    name = models.CharField(max_length= 100)
    description = models.CharField(max_length = 255, blank = True, null =True)
    slug = models.SlugField(max_length=100 ,unique=True, blank= True)
    percent = models.FloatField(null = True)
    fix_amount = models.FloatField(null = True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null = True)
    is_activate = models.BooleanField(default=True)

    product = models.ManyToManyField(Product, db_column='product_id', blank=True, related_name="promotions")
    category = models.ManyToManyField(Category, db_column='category_id', blank=True, related_name="promotions")
    collection = models.ManyToManyField(Collection, db_column='collection_id', blank=True, related_name="promotions")
