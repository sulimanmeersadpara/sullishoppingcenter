from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from accounts.models import User
from accounts import forms
from django.contrib import messages
from categories.models import gender
from django.contrib import messages
def delete_employee(request,id):
    try:
        employee = get_object_or_404(User,id=id)
        employee.profile_image.delete(save=False)

        # Delete the DB record
        employee.delete()

        messages.warning(request, "Employee deleted successfully")
        return redirect('employee_list')
    except:
        pass
    messages.warning(request, "Employee couldn't delete")
    return redirect('employee_list')
def update_employee(request,id):
    try:    
        employee = get_object_or_404(User,id=id)
        if request.method=="POST":        
            errors={}
            values={}
            emp_name=request.POST['emp_name']
            emp_fname=request.POST['emp_fname']
            emp_CNIC=request.POST['emp_CNIC']
            emp_email=request.POST['emp_email']
            emp_phone=request.POST['emp_phone']
            emp_gender=int(request.POST['gender'])
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
            if not emp_fname:
                pass
            else:
                if forms.formValidations.is_valid_username(emp_name):
                    pass
                else:
                    errors.update({"emp_name":"invalid employee name please use  characters and numbers only OR you can keep it empty if you want"})   
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
                errors.update({"emp_job":"invalid job title please use chargacters and numbers only"})   
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
        
            if(errors):
                return render(request,'employee/update_employee.html',{'errors':errors,'values':values})
            else:
                emp_gender=get_object_or_404(gender,g_id=int(emp_gender))  
                employee.username=emp_email
                employee.first_name=emp_name
                employee.email=emp_email
                employee.is_active=status
                employee.date_joined=emp_hiring_date
                employee.CNIC=emp_CNIC
                employee.job_title=emp_job
                employee.salary=emp_salary
                employee.address=emp_address
                employee.nationality=emp_nationality
                employee.bank_account_number=emp_bank
                employee.phone=emp_phone
                employee.DOB=emp_DOB
                employee.parent=emp_fname
                employee.gender_id=emp_gender
                employee.save()
                messages.success(request,"Employee updated Successfully")
                return redirect('employee_list')
        return render(request,'employee/update_employee.html',{'employee':employee})
    except Exception as e:
        messages.warning(request,"something went wrong")
        messages.warning(request,e)
        return render(request,'home/notPageFoundError.html')
        
    
    
