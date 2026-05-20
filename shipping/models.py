from accounts.models import User
from django.db import models
# Create your models here.
class cities(models.Model):
    city_name=models.CharField(max_length=50)
   
class country(models.Model):
    country_name=models.CharField(max_length=50)

class shipping_areas(models.Model):
    area_name=models.CharField(max_length=100)
    postal_code=models.CharField(max_length=20)
    base_charge=models.IntegerField(default=0)#cost for delivering at least 1 item to this area( eg. Rs.200 for first item)
    additional_item_charge=models.IntegerField(default=0)#extra cost per item after the first (e.g. Rs. 20 per extra item)
    max_charges=models.IntegerField(default=0)# max shipping charges for this area, i mean after 10,000 the remaing products will be free deleiver
    estimated_time=models.CharField(max_length=100)# 1 day, 3 hourse etc
    is_active =models.BooleanField(default=True)# it meanse the delevery for that is exist
    city=models.ForeignKey(cities,on_delete=models.CASCADE,related_name='cities_shipping_areas')
    country_name=models.ForeignKey(country,on_delete=models.CASCADE,related_name='shipping_areas_country')
    advance_payment_percent=models.IntegerField(default=0)

class customer_shipping_location(models.Model):
    phone_number=models.CharField(max_length=30)
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='shipping_user_id')
    shipping_area_id=models.ForeignKey(shipping_areas,on_delete=models.CASCADE,related_name='customer_shipping_area')
    address1=models.CharField(max_length=200)
    address2=models.CharField(max_length=200)
    deleivery_charges=models.IntegerField(default=0)
    product_price=models.IntegerField(default=0)
    total=models.IntegerField(default=0)
    advance_pay=models.IntegerField(default=0)
    delevery_option=models.CharField(max_length=20,default='now')
    date_ordered = models.DateTimeField(blank=True, null=True)
    notes=models.TextField(null=True)
    online_paid=models.IntegerField(default=0)
    rest_for_delvery=models.IntegerField(default=0)


    