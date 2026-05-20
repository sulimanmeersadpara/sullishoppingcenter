from django.shortcuts import render,HttpResponse,redirect
from categories.models import gender
from accounts import forms
from django.contrib.auth.hashers import make_password, check_password
from products.views2 import generate_unique_filename
from django.shortcuts import get_object_or_404
from accounts.models import User
from django.contrib import messages
def add_employee(request):
    try:
        if(request.method=="POST"):
            errors={}
            values={}
            emp_name=request.POST['emp_name']
            emp_fname=request.POST['emp_fname']
            emp_password=request.POST['emp_password']
            emp_confirm_password=request.POST['emp_confirm_password']
            emp_CNIC=request.POST['emp_CNIC']
            emp_email=request.POST['emp_email']
            emp_phone=request.POST['emp_phone']
            emp_gender=request.POST['gender']
            emp_DOB=request.POST['emp_DOB']
            emp_job=request.POST['emp_job']
            emp_hiring_date=request.POST['emp_hiring_date']
            emp_salary=int(request.POST['emp_salary'])
            status = int(request.POST.get('status', '0'))
            emp_address=request.POST['emp_address']
            emp_nationality=request.POST['emp_nationality']
            emp_bank=request.POST['emp_bank']
            values.update({'emp_name':emp_name,'emp_fname':emp_fname,'emp_CNIC':emp_CNIC,'emp_email':emp_email,'emp_phone':emp_phone,'gender':emp_gender,'emp_DOB':emp_DOB,'emp_job':emp_job,
                        'emp_hiring_date':emp_hiring_date,'emp_salary':emp_salary,'status':status,'emp_address':emp_address,'emp_nationality':emp_nationality,'emp_bank':emp_bank})
            if(request.FILES.get('emp_image')):
                emp_image=request.FILES.get('emp_image')
            else:
                errors.update({"emp_image":"please input atleast one image(jpg,jpeg or png are allowed)"})   
            if not emp_password:
                
                errors.update({"emp_password":"please enter password"}) 
            if not emp_confirm_password:
                
                errors.update({"emp_confirm_password":"please enter confirm password"}) 
            if forms.formValidations.is_valid_username(emp_name):
                pass
            
            else:
                errors.update({"emp_name":"invalid employee name please use characters and numbers only"})   
            if not emp_fname:
                pass
            else:
                if forms.formValidations.is_valid_username(emp_fname):
                    pass
                else:
                    errors.update({"emp_fname":"invalid employee parent name please use  characters and numbers only OR you can keep it empty if you want"})   
            if forms.formValidations.is_valid_username(emp_nationality):
                pass
            else:
                errors.update({"emp_nationality":"invalid nationality please use  characters and numbers only"})  
            
            if forms.formValidations.is_valid_mail(emp_email):
                pass
            else:
                errors.update({"emp_email":"invalid email "})       

            if forms.formValidations.is_valid_username(emp_job):
                pass
            else:
                errors.update({"emp_job":"invalid job title please use characters and numbers only"})   
            if forms.formValidations.is_valid_CNIC(emp_address):
                pass
            else:
                errors.update({"emp_address":"invalid address please use  characters and numbers ,dots ,commas , hyphens and underscore"})   
            if forms.formValidations.is_valid_CNIC(emp_CNIC):
                pass
            else:
                errors.update({"emp_CNIC":"invalid ID Card Number please use characters and numbers ,dots ,commas , hyphens and underscores"})
            if forms.formValidations.is_valid_CNIC(emp_bank):
                pass
            else:
                errors.update({"emp_bank":"invalid bank account Number please use characters and numbers ,dots ,commas , hyphens and underscores"}) 
            if forms.formValidations.password_match(emp_password,emp_confirm_password):
                pass
            else:
                errors.update({"emp_password":"password and confirm password are not matched"}) 
                errors.update({"emp_confirm_password":"password and confirm password are not matched"}) 
            
            if(errors):
                return render(request,'employee/add_employee.html',{'errors':errors,'values':values})
            else:
                emp_gender=get_object_or_404(gender,g_id=int(emp_gender))
                new_name = generate_unique_filename(emp_image.name)
                emp_image.name=new_name
                if not User.objects.filter(username=emp_email).exists():
                    user = User(username=emp_email, email=emp_email,first_name=emp_name,parent=emp_fname,is_staff=1,is_active=status,date_joined=emp_hiring_date,CNIC=emp_CNIC,
                                job_title=emp_job,salary=emp_salary,address=emp_address,nationality=emp_nationality,bank_account_number=emp_bank,profile_image=emp_image,
                                phone=emp_phone,DOB=emp_DOB,gender_id=emp_gender)
                    user.set_password(emp_password)
                    user.save()
                    messages.success(request,"New Employee added Successfully")
                    return redirect('employee_list')
                else:
                    errors.update({'emp_email':'this email is already exist'})
        genders=gender.objects.all()
        return render(request,'employee/add_employee.html',{'genders':genders})
    except Exception as e:
        messages.warning(request,"something went wrong")
        messages.warning(request,e)
        return render(request,'home/notPageFoundError.html')
# Create your views here.
def employee_list(request):
    try:
        data=User.objects.filter(is_staff=1)
        return render(request,'employee/employee_list.html',{'emp_data':data})
    except Exception as e:
        messages.warning(request,"something went wrong")
        messages.warning(request,e)
        return render(request,'home/notPageFoundError.html')