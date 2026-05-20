from django.shortcuts import render,redirect,HttpResponse
from .models import shipping_areas,country,cities
from django.contrib import messages
from accounts.utils import has_permission
def payment_percentage_check(percentage):
    if(percentage<0 or percentage>100):
        return False
    return True
def add_shipping_areas(request):
    try:
        if has_permission(request.user, 'add_shipping_areas', 'shipping'):
            errors={}
            if request.method=='POST':
                area_name=request.POST['area_name']
                postal_code=request.POST['postal_code']
                base_charge=request.POST['base_charge']
                additional_item_charge=request.POST['additional_item_charge']
                max_charges=request.POST['max_charges']
                estimated_time=request.POST['estimated_time']
                status = int(request.POST.get('status', '0'))
                city=request.POST['city']
                country_name=country.objects.first()
                city=cities.objects.get(id=city)
                advance_payment_percentage = int(request.POST['advance_payment_percentage'])
                if(payment_percentage_check(advance_payment_percentage)):
                    shipping_obj=shipping_areas(area_name=area_name,postal_code=postal_code,base_charge=base_charge,additional_item_charge=additional_item_charge,max_charges=max_charges,estimated_time=estimated_time,is_active=status,city=city,country_name=country_name,advance_payment_percent=advance_payment_percentage)
                    shipping_obj.save()
                    messages.success(request,'the new shipping postal address added successfully')
                    return redirect('shipping_menipulations')
                else:
                    errors.update({'payment':'the advance payment percentage should be between 0 to 100'})
            cities_list=cities.objects.all()
            return render(request,'shipping/add_shipping_areas.html',{'cities':cities_list,'errors':errors})
        else:
            return redirect('home')
        
    except Exception as e:
        messages.warning(request,"something went wrong")
        messages.warning(request,e)
        return render(request,'home/notPageFoundError.html')
def delete_shipping(request,id):
    try:
        if has_permission(request.user, 'delete_shipping_areas', 'shipping'):
            shipping_area=shipping_areas.objects.get(id=id)
            shipping_area.delete()
            messages.warning(request,'shipping area deleted successfully')
            return redirect('shipping_menipulations')
        else:
            return redirect('home')
    except Exception as e:
        messages.warning(request,"something went wrong")
        messages.warning(request,e)
        return render(request,'home/notPageFoundError.html')
def update_shipping(request,id):
    try:
        if has_permission(request.user, 'change_shipping_areas', 'shipping'):
            shipping_area=shipping_areas.objects.get(id=id)
            if request.method=='POST':
                area_name=request.POST['area_name']
                postal_code=request.POST['postal_code']
                base_charge=request.POST['base_charge']
                additional_item_charge=request.POST['additional_item_charge']
                max_charges=request.POST['max_charges']
                estimated_time=request.POST['estimated_time']
                status = int(request.POST.get('status', '0'))
                city=request.POST['city']
                country_name=country.objects.first()
                city=cities.objects.get(id=city)

                shipping_area.area_name=area_name
                shipping_area.postal_code=postal_code
                shipping_area.base_charge=base_charge
                shipping_area.additional_item_charge=additional_item_charge
                shipping_area.max_charges=max_charges
                shipping_area.estimated_time=estimated_time
                shipping_area.is_active=status
                shipping_area.city=city
                shipping_area.country_name=country_name
                shipping_area.save()
                messages.success(request,'shipping area updated successfully')
                return redirect('shipping_menipulations')
            
            cities_list=cities.objects.all()
            shipping_area=shipping_areas.objects.get(id=id)
            return render(request,'shipping/update_shipping_admin.html',{'shipping_area':shipping_area,'cities':cities_list})
        else:
            return redirect('home')
    except Exception as e:
        messages.warning(request,"something went wrong")
        messages.warning(request,e)
        return render(request,'home/notPageFoundError.html')