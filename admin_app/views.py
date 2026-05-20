from django.shortcuts import render,HttpResponse,redirect
from admin_app.models import admin_table
from .forms import formValidations
from .utiles import sendmail
from django.contrib.auth.hashers import check_password
from django.http import HttpResponseForbidden

def admin_auth_page(request):
        if request.method=='POST':
            try:
                errors={}
                email=request.POST["email"]
                password=request.POST["password"]
                if formValidations.is_valid_username(email) == False:
                    errors.update({'invalid_username':'invalide username'})
                else:
                    try:
                
                        admin = admin_table.objects.get(admin_email=email)
                    
                        if check_password(password, admin.password):
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
            
            if(errors):
                return render(request,'admin/admin_auth_page.html',{'errors':errors})

            
            
        return render(request,'admin/admin_auth_page.html')
    
    
# Create your views here.