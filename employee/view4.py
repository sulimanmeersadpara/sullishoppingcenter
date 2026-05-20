from django.shortcuts import HttpResponse,redirect,render
from products.views2 import generate_unique_filename
from django.shortcuts import get_object_or_404
from accounts.models import User
from django.contrib import messages
import os
from django.conf import settings

from django.contrib.auth import authenticate
def employee_account(request):
    try:
        if(request.user.is_staff==1):
            return render(request,'employee/employee_account.html')
        else:
            return redirect('home')
    except Exception as e:
        messages.warning(request,"something went wrong")
        messages.warning(request,e)
        return render(request,'home/notPageFoundError.html')
    
def change_profile_image(request):
    try:
        if(request.user.is_staff==1):
            
        
            if request.method == "POST":
                user = get_object_or_404(User, id=request.user.id , is_staff=1)
            
                
                # Example: Only handling image update here
                if request.FILES.get("emp_image"):
                    new_image = request.FILES["emp_image"]

                    # Delete old image if exists
                    
                    if user.profile_image:
                        old_path = os.path.join(settings.MEDIA_ROOT, user.profile_image.name)
                        if os.path.exists(old_path):
                            os.remove(old_path)

                    # Generate unique filename for new image
                    new_name = generate_unique_filename(new_image.name)
                    new_image.name = new_name

                    # Assign and save
                    user.profile_image = new_image
                    user.save()

                    messages.success(request, "Profile image updated successfully")
                    return redirect("dashboard")
                else:
                    messages.warning(request,'please upload an image')
                    return redirect('change_profile_image')
            else:
                return render(request,'employee/update_profile_image.html')
        else:
            return redirect('home')
    except Exception as e:
        messages.warning(request,"something went wrong")
        messages.warning(request,e)
        return render(request,'home/notPageFoundError.html')
def change_password(request):
    try:
        if(request.method=="POST"):
            errors=0
            old_password=request.POST['old_password']
            new_password=request.POST['new_password']
            confirm_password=request.POST['confirm_password']
            if not old_password:
                errors=1
                messages.warning(request,'please input old password')
            if not new_password:
                errors=1
                messages.warning(request,'please input new password')
            if not confirm_password:
                errors=1
                messages.warning(request,'please input confirm password')
            if(new_password == confirm_password):
                pass
            else:
                errors=1
                messages.warning(request,'password and confirm password are not same')
            user = authenticate(username=request.user.username, password=old_password)
            if user is None:
                errors=1
                messages.warning(request,'the old password is wrong')
            if(errors==1):
                return redirect('employee_account')
            else:
                #user = User.objects.get(username=request.user.username)
                request.user.set_password(new_password)
                request.user.save()
                messages.success(request,'password changed successfully')
                return redirect('employee_account')
        else:
            return redirect('home')
    except Exception as e:
        messages.warning(request,"something went wrong")
        messages.warning(request,e)
        return render(request,'home/notPageFoundError.html')