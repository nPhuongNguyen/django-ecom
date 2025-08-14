from django.db import models
class Voucher(models.Model):
    voucher_code = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length= 100)
    description = models.CharField(max_length = 255, blank = True, null =True)
    percent = models.FloatField(null = True)
    fix_amount = models.FloatField(null = True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null = True)
    is_activate = models.BooleanField(default=True)

