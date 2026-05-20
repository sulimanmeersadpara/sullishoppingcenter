from django.db import models
from products.models import product
from accounts.models import User

   

class Orderhistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    products_detail=models.TextField(default=None)
    total_price=models.IntegerField(default=0)
    shipping_address = models.CharField(default=None,max_length=400)
    postal_code=models.CharField(default=None,max_length=50)
    city=models.CharField(default=None,max_length=50)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    date_ordered = models.DateTimeField(blank=True)
    is_shift=models.BooleanField(default=0)
    def __str__(self):
        return f"Order = {str(self.id)}"