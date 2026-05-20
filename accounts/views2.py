from django.shortcuts import render,redirect,HttpResponse
from accounts.models import User
from django.contrib import messages
from django.contrib.auth import login
from .utils import send_email_to_client
def verify(request):
    if request.method=="POST":
        email=request.POST['email']
        code=request.POST['code']
        record=User.objects.get(email=email)
        if(record.code==code):
            record.is_verified=1
            record.save()
            login(request, record)
            request.session['NumberOfCartItems']=0
            # Automatically log in the user after signup
            messages.success(request, f"you have signup successfully  {record.first_name}")
            #return HttpResponse("you have signup successfully")
            previous_url = request.session.get('previous_url')
            if 'path' in request.session:
                return redirect(request.session['path'])
            else:
                
                return redirect('home')
        else:
            
            messages.warning(request, "you are not verified")
            return redirect('signup')
        
    else:
        return redirect('home')
def forget_password_gmail_for_otp(request):
    if(request.method=="POST"):

        email=request.POST['email']
        if(User.objects.filter(username=email,is_staff=0).exists()):
            
            status,otp=send_email_to_client(email)
            user=User.objects.get(username=email,is_staff=0)
            user.code=str(otp)
            user.save()
            return render(request,'accounts/forget_password_verify_code_page.html',{'email':email})
        else:
            messages.warning(request,'there is no account of this email')

    return render(request,'accounts/forget_password_gmail_for_otp.html')

def forget_password_verify_code_page(request):
    if(request.method=="POST"):
        email=request.POST['email']
        otp=request.POST['OTP']
        user=User.objects.get(username=email)
        if(user.code==str(otp)):
            user.is_verified=1
            user.save()
            messages.success(request,'conguratulations!Your OTP authentication completed successfully')
            return render(request,'accounts/forget_password_change_password.html',{'email':email})
        else:
            messages.warning(request,'The OTP you entered is wrong')
            return redirect('siginin')
    else:
        return redirect('home')
