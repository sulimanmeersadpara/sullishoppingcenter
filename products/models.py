from django.db import models
from categories.models import child_category,gender
from django.http import HttpResponse
# Create your models here.

class ColorVariant(models.Model):
    color_name=models.CharField(max_length=100)
    color_code=models.CharField(max_length=100)

    def __str__(self)-> str:
            return self.color_name#it is returning the name of product in admin site e.g shirt coat. without this the object was returning

class SizeVariant(models.Model):
    size_name = models.CharField(max_length=100)
    def __str__(self)-> str:
            return self.size_name#it is returning the name of product in admin site e.g shirt coat. without this the object was returning

class product(models.Model):
    p_id=models.BigAutoField(auto_created=True, primary_key=True, serialize=False,)
    p_name=models.CharField(max_length=100)
    p_compony=models.CharField(max_length=100)
    p_description=models.CharField(max_length=1500)
    p_child_category=models.ForeignKey(child_category,on_delete=models.CASCADE,related_name='p_child_category')
    min_price=models.IntegerField(default=0)
    max_price=models.IntegerField(default=0)
    p_gender=models.ForeignKey(gender,on_delete=models.CASCADE,related_name='product_gender')
    slug=models.SlugField()
    average_star_rate=models.DecimalField(
    max_digits=2,
    decimal_places=1,
    default=0.0)
    rate_persons=models.IntegerField(default=0)
    

class product_variant(models.Model):
    pv_id=models.BigAutoField(auto_created=True, primary_key=True, serialize=False)
    product=models.ForeignKey(product,on_delete=models.CASCADE,related_name='product_product_variant')
    size=models.ForeignKey(SizeVariant,on_delete=models.CASCADE,related_name='size_product_variant')
    color=models.ForeignKey(ColorVariant,on_delete=models.CASCADE,related_name='color_product_variant')
    price=models.IntegerField(default=0)
    quantity=models.IntegerField(default=0)
    p_is_sale=models.BooleanField(default=False)
    sale_price=models.IntegerField(default=0)
    is_available=models.BooleanField(default=0)

class product_image(models.Model):

    i_id=  models.BigAutoField(auto_created=True, primary_key=True, serialize=False,)
    image=models.ImageField(upload_to='images')
    product_id=models.ForeignKey(product,on_delete=models.CASCADE,related_name='p_image')
    product_variant_id=models.ForeignKey(product_variant,on_delete=models.CASCADE,related_name='product_variant')
    