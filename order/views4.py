from django.shortcuts import render,redirect,HttpResponse
from shipping.models import customer_shipping_location
from add_to_card.models import Card
from .models import order,orders_products
import random
from .models import order
from django.contrib import messages

def decrease_stock(request,id):

        order_obj=order.objects.get(id=id)
        if(order_obj.decrease_stack is 0):
            for ob in order_obj.order_order.all():
                quantity=ob.quantity
                ob.c_product_variant.quantity=ob.c_product_variant.quantity-quantity
                ob.c_product_variant.save()
                order_obj.decrease_stack=1
                order_obj.save()
            messages.success(request,'the quantities have decreased successfully')    
            return redirect('view_order',id=id)
        else:
             messages.warning(request,'sory this item quantity is already decreased from stock')
             return redirect('home')
    
        