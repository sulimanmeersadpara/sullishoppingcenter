from django.shortcuts import render,HttpResponse,redirect
from admin_app.models import admin_table
from .forms import formValidations
from django.contrib.auth import login,authenticate
from django.contrib.auth.hashers import make_password,check_password
from datetime import datetime
from .utiles import sendmail

def emailforcode(request):
    if request.method=='POST':
        try:
            errors={}
            email=request.POST["email"].strip()
            DOB=request.POST['DOB'].strip()
            if formValidations.is_valid_username(email) == False:
                errors.update({'invalid_username':'invalide username'})
            
            else:
                try:
                    admin = admin_table.objects.get(admin_email=email)
                    dob_obj = datetime.strptime(DOB, "%Y-%m-%d").date()
                    if admin.admin_dob==dob_obj:
                        status,otp=sendmail()
                        admin.code=otp
                        admin.save()
                        return redirect('sixdigitcodesubmit', email=email)
                    else:
                        errors.update({'wrongpassword':'you entered wrong password'})   
                except:
                    errors.update({'usernamenotfound':'username is not found'})  
             
        except:
            errors.update({'somethingwrong':'some thing went wrong'})
        if errors:
            return render(request,'admin/admin_auth_page.html',{'errors':errors})
        #return HttpResponse(errors)
    
    return render(request,'admin/emailfor6digitcode.html')
def sixdigitcodesubmit(request,email):
    if (request.method=='POST'):
        errors={}
        email= request.POST['email']
        otp_code=int(request.POST['otp_code'])
        
        try:
            admin = admin_table.objects.get(admin_email=email)
            if(admin.code == otp_code):
                return HttpResponse('you are true admin')
            else:
                return HttpResponse('you are not true admin and the next step is to redirect you in admin auth page')
        except:
            errors.update({'usernamenotfound':'username is not found'})    
        
    return render(request,'admin/6digitcodesubmit.html',{'email':email})
