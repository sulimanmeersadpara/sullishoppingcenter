from django.shortcuts import render,HttpResponse,redirect
from .models import order
from accounts.utils import has_permission
from django.contrib import messages
def orderslist(request):
    try:
        if has_permission(request.user, 'view_order', 'order'):
            total_uncomplete_orders=order.objects.filter(completes_status=0)
            orders=order.objects.filter(admin_read_status=0).count()
            return render(request,'order/ordersList.html',{'orders':orders,'total_uncomplete_orders':total_uncomplete_orders})
        else:
              return redirect('home')
    except Exception as e:
        messages.warning(request,"something went wrong")
        messages.warning(request,e)
        return render(request,'home/notPageFoundError.html')
        
