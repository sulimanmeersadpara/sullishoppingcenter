from django.shortcuts import render,redirect,HttpResponse
from .models import Orderhistory
from shipping.models import customer_shipping_location
from add_to_card.models import Card
from order.models import order
from django.contrib import messages
from review.models import products_review

def history(request,id):
    try:
        order_obj=order.objects.get(id=id)
        for o_o in order_obj.order_order.all():
            p_r=products_review(user=order_obj.user,c_product=o_o.c_product,c_product_variant=o_o.c_product_variant,quantity=o_o.quantity,price=o_o.price)
            p_r.save()
        if order_obj.decrease_stack is 0:
           
            for ob in order_obj.order_order.all():
                quantity=ob.quantity
                ob.c_product_variant.quantity=ob.c_product_variant.quantity-quantity
                ob.c_product_variant.save()
                order_obj.decrease_stack=1
                order_obj.save()
        products_detail=''
        card_data=Card.objects.filter(c_user=request.user)
        
        user=order_obj.user
        for item in order_obj.order_order.all():
            products_detail=products_detail+item.c_product.p_name+'-'+item.c_product.p_compony+'-'+item.c_product.p_child_category.c_c_name+'-'+item.c_product.p_gender.g_name+'-'+str(item.price)+'-'+item.c_product_variant.size.size_name+'-'+item.c_product_variant.color.color_name+'-'+str(item.quantity)+',,-,,'
        
        # customer_data_shipping_location=customer_shipping_location.objects.get(user=request.user) 
        full_name=user.first_name  
        
        email=user.email
        address=order_obj.shipping_address
        city=order_obj.shipping_area_id.city.city_name
        postal_code=order_obj.shipping_area_id.postal_code
        total_price=order_obj.total
        amount_paid=order_obj.online_paid
        date_ordered=order_obj.date_ordered
        add_history=Orderhistory(user=request.user,full_name=full_name,email=email,products_detail=products_detail,total_price=total_price,shipping_address=address,postal_code=postal_code,city=city,amount_paid=amount_paid,is_shift=1,date_ordered=date_ordered)
        add_history.save()
        order_obj.delete()
        return redirect('orderslist')
    except Exception as e:
        messages.warning(request,"something went wrong")
        messages.warning(request,e)
        return render(request,'home/notPageFoundError.html')
        