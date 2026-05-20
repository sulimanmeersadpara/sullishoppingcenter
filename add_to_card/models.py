
from django.db import models
from products.models import product,product_variant
from accounts.models import User
# Create your models here.
class Card(models.Model):
    c_id= models.BigAutoField(auto_created=True, primary_key=True, serialize=False)
    c_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user')
    c_product=models.ForeignKey(product,on_delete=models.CASCADE,related_name='product')
    c_product_variant=models.ForeignKey(product_variant,on_delete=models.CASCADE,related_name='card_product_variant')
    quantity=models.IntegerField(default=1)
    price=models.IntegerField(default=0)
    
class coupon_discount(models.Model):
    cd_id= models.BigAutoField(auto_created=True, primary_key=True, serialize=False)
    code=models.CharField(max_length=50, unique=True)
    max_numbers_of_products=models.IntegerField(default=1)
    max_price=models.IntegerField(default=1)
    discount_percentage=models.IntegerField(default=0)
    is_active_coupon = models.BooleanField(default=True)
    usage_limit = models.IntegerField(default=1)  # Total times this coupon can be used
    def __str__(self):
        return self.code



  
# Create your models here.
