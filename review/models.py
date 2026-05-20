from django.db import models

# Create your models here.
from django.db import models
from accounts.models import User
from shipping.models import customer_shipping_location,shipping_areas
from products.models import product,product_variant
# Create your models here.
class products_review(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    c_product=models.ForeignKey(product,on_delete=models.CASCADE)
    c_product_variant=models.ForeignKey(product_variant,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    price=models.IntegerField(default=0)
    comment=models.TextField(max_length=500, blank=True, default='')
    star_rate=models.IntegerField(default=0)
    comment_or_not=models.BooleanField(default=0)
    




    


