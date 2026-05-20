from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import Permission
from accounts.models import User
from django.contrib import messages
# Create your views here.
def permissions(request):
    try:
        if(request.user.is_superuser==1 ):
            if(request.method=='POST'):
                permission_id=request.POST['permission']
                employee_id=request.POST['employee']
                employee = User.objects.get(id=employee_id)
                permission = Permission.objects.get(id=permission_id)
                employee.user_permissions.add(permission)
                employee.save()
                # employee.user_permissions.remove(permission) to remove permissions
                messages.success(request,'permission assigned successfully')
                return redirect('permissions')
            perms = Permission.objects.filter(
            content_type__model__in=['user','product' , 'sizevariant' , 'colorvariant' , 'child_category' , 'gender' , 'parent_category','order','shipping_areas']
        ).order_by('name')
            employees=User.objects.filter(is_staff=1,is_active=1)
            return render(request,'permissions/permissions.html',{'permissions':perms,'employees':employees})
        else:
            return redirect('home')
    except Exception as e:
        messages.warning(request,"something went wrong")
        messages.warning(request,e)
        return render(request,'home/notPageFoundError.html')
   
def delete_permission(request,perm_id,emp_id):
    try:
        if(1):    
            employee = User.objects.get(id=emp_id)
            permission = Permission.objects.get(id=perm_id)
            employee.user_permissions.remove(permission)
            messages.success(request,'permission removed successfully')
            return redirect('permissions')
        else:
            return redirect('home')
    except Exception as e:
        messages.warning(request,"something went wrong")
        messages.warning(request,e)
        return render(request,'home/notPageFoundError.html')
   
