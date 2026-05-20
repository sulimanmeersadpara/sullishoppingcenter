from django.db import models
from accounts.models import User
from shipping.models import customer_shipping_location,shipping_areas
from products.models import product,product_variant
# Create your models here.
class order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='order_user')
    shipping_address=models.CharField(max_length=200)
    online_paid=models.IntegerField(default=0)
    total=models.IntegerField(default=0)
    remaining_paid=models.IntegerField(default=0)
    decrease_stack=models.IntegerField(default=0)
    completes_status=models.BooleanField(default=0)#completed or not completed
    admin_read_status=models.BooleanField(default=0)
    admin_stored_history=models.BooleanField(default=0)
    user_watched_success_page=models.BooleanField(default=0)
    delevery_option=models.CharField(max_length=20,default='now')
    date_ordered = models.DateTimeField()
    phone_number=models.CharField(max_length=30)
    DevelveryCode=models.CharField(max_length=20,default='none',null=True)
    shipping_area_id=models.ForeignKey(shipping_areas,on_delete=models.CASCADE,related_name='order_shipping_area')
    product_price=models.IntegerField(default=0)
    notes=models.TextField(null=True)

class orders_products(models.Model):
    orders=models.ForeignKey(order,on_delete= models.CASCADE,related_name='order_order')
    c_product=models.ForeignKey(product,on_delete=models.CASCADE,related_name='order_product')
    c_product_variant=models.ForeignKey(product_variant,on_delete=models.CASCADE,related_name='order_product_variant')
    quantity=models.IntegerField(default=1)
    price=models.IntegerField(default=0)
    

