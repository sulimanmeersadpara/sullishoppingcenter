from django.shortcuts import render,redirect,HttpResponse
from shipping.models import customer_shipping_location
from add_to_card.models import Card
from .models import order,orders_products
import random
from .models import order
from django.contrib import messages
def order_def(request):
    try:
        customer_shipping_obj=customer_shipping_location.objects.get(user=request.user)
        address=customer_shipping_obj.address1+' , '+customer_shipping_obj.address2+' , '+customer_shipping_obj.shipping_area_id.city.city_name
        online_paid=customer_shipping_obj.online_paid
        total=customer_shipping_obj.total
        remaining_paid=total-online_paid
        delevery_option=customer_shipping_obj.delevery_option
        date_ordered=customer_shipping_obj.date_ordered
        phone_number=customer_shipping_obj.phone_number
        product_price=customer_shipping_obj.product_price
        notes=customer_shipping_obj.notes
        code = str(random.randint(10000000, 999999999))
        request.session['delveiry_code']=code
        save_order=order(user=request.user,shipping_address=address,online_paid=online_paid,total=total,remaining_paid=remaining_paid,delevery_option=delevery_option,product_price=product_price,date_ordered=date_ordered,phone_number=phone_number,shipping_area_id=customer_shipping_obj.shipping_area_id,notes=notes,DevelveryCode=code)
        save_order.save()
        products=Card.objects.filter(c_user=request.user)
        for p in products:
            save_order_products=orders_products(orders=save_order,c_product=p.c_product,c_product_variant=p.c_product_variant,quantity=p.quantity,price=p.price)
            save_order_products.save()
        return redirect('send_order_confirmation_email')
    except Exception as e:
        messages.warning(request,"something went wrong")
        messages.warning(request,e)
        return render(request,'home/notPageFoundError.html')
   

def view_order(request,id):
    try:
        order_obj=order.objects.get(id=id)
        order_obj.admin_read_status=1
        order_obj.save()
        orders=order.objects.filter(admin_read_status=0).count()
        
        return render(request,'order/orderview.html',{'order_obj':order_obj,'orders':orders})
    except Exception as e:
        messages.warning(request,"something went wrong")
        messages.warning(request,e)
        return render(request,'home/notPageFoundError.html')
   

        

