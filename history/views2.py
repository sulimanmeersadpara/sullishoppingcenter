from django.shortcuts import render,redirect,HttpResponse
from add_to_card.models import Card
from shipping.models import customer_shipping_location
from order.models import order,orders_products
from django.contrib import messages
def success_checkout(request):
    try:
        user_order = list(order.objects.filter(user=request.user, user_watched_success_page=0))
        
        customer_shipping_obj = customer_shipping_location.objects.get(user_id=request.user)
        total_price = customer_shipping_obj.total

        all_products = orders_products.objects.filter(orders__in=user_order)

        for u_o in user_order:
            u_o.user_watched_success_page = 1
            u_o.save()

        return render(request,'history/success_checkout.html',{
            'products': all_products,
            'customer_shipping_obj': customer_shipping_obj,
            'total_price': total_price
        })
    except Exception as e:
        messages.warning(request,"something went wrong")
        messages.warning(request,e)
        return render(request,'home/notPageFoundError.html')