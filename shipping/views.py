from django.shortcuts import render,HttpResponse,redirect
from .models import shipping_areas

from accounts.utils import has_permission
from django.contrib import messages
def shipping_menipulations(request):
    try:
        if has_permission(request.user, 'add_shipping_areas', 'shipping') or has_permission(request.user, 'delete_shipping_areas', 'shipping') or has_permission(request.user, 'change_shipping_areas', 'shipping') or has_permission(request.user, 'view_shipping_areas', 'shipping'):
            shipping_areas_list=shipping_areas.objects.all()
            return render(request,'shipping/shipping_menipulations.html',{'shipping_areas_list':shipping_areas_list})
        else:
            return redirect('home')
    except Exception as e:
        messages.warning(request,"something went wrong")
        messages.warning(request,e)
        return render(request,'home/notPageFoundError.html')