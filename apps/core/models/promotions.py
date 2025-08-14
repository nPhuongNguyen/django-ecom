from django.db import models
from django.utils.text import slugify
class Promotion(models.Model):
    name = models.CharField(max_length= 100)
    description = models.CharField(max_length = 255, blank = True, null =True)
    slug = models.SlugField(max_length=100 ,unique=True, blank= True)
    percent = models.FloatField(null = True)
    fix_amount = models.FloatField(null = True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null = True)
    is_activate = models.BooleanField(default=True)

    product = models.ManyToManyField('core.Product', blank=True)
    category = models.ManyToManyField('core.Category', blank=True)
    collection = models.ManyToManyField('core.Collection', blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Promotion.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

