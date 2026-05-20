from django.db import models
from datetime import date
# Create your models here.
class admin_table(models.Model):
    password=models.CharField(max_length=100)
    admin_name=models.CharField(max_length=100)
    admin_email=models.EmailField(max_length=100)
    admin_dob = models.DateField(
        default=date(2000,9,27),
        verbose_name="Date of Birth"
    )
    code=models.IntegerField(default=000000)
