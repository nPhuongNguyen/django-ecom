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
    category = models.ForeignKey('core.Category', on_delete=models.PROTECT, blank=True, null = True,related_name="products")
    collection = models.ManyToManyField('core.Collection', blank=True,related_name='products')

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

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="variants")
    name = models.CharField(max_length=255,null=True)
    img = models.CharField(max_length = 200,null= True, blank= True)
    sku = models.CharField(max_length=50, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock_qty = models.IntegerField(default=0)
    is_deleted = models.BooleanField(default=False)

class Option(models.Model):
    name = models.CharField(max_length=50)
    is_deleted = models.BooleanField(default=False)


class OptionValue(models.Model):
    option = models.ForeignKey(Option, on_delete=models.CASCADE, related_name="values")
    value = models.CharField(max_length=50)

class VariantOptionValue(models.Model):
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name="option_values")
    option_value = models.ForeignKey(OptionValue, on_delete=models.CASCADE)
    class Meta:
        unique_together = ('variant', 'option_value')