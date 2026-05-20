
from django.shortcuts import render,HttpResponse,redirect
from .utiles import has_permission_for_dashboard
from django.http import HttpResponseForbidden
from django.contrib import messages
from order.models import order
def dashboard(request):
    #try:
        if has_permission_for_dashboard(request.user):
                orders=order.objects.filter(admin_read_status=0).count()
                

                return render(request,'admin/dashboard.html',{'orders':orders})
        return redirect('home')
    #except:
        return redirect('home')