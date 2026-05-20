from django.shortcuts import HttpResponse,render,redirect
from django.contrib import messages
from accounts.models import User
def forget_password_change_password(request):
    if(request.method=="POST"):
        email=request.POST['email']
        password=request.POST['password']
        confirm_password=request.POST['confirm_password']
        if(password== confirm_password):
            user = User.objects.get(username=email)
            user.set_password(password)  # Hash the password
            user.save()
            messages.success(request,'password changed successfully, now you can login')
            return redirect('siginin')
        else:
            messages.warning(request,'passwords and confirm password did not match')
            return render(request,'accounts/forget_password_change_password.html',{'email':email})
    return redirect('home')