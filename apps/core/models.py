from django.db import models
from django.utils.text import slugify
# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=150, unique=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    img = models.CharField(max_length=255, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    category = models.ForeignKey('Category', on_delete=models.PROTECT, null=True, blank=True)
    collection = models.ManyToManyField('Collection', null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

class Category(models.Model):
    name = models.CharField(max_length=100)
    sku = models.CharField(max_length=150, unique=True)

class Collection(models.Model):
    name = models.CharField(max_length=100)
    sku = models.CharField(max_length=150, unique=True)

