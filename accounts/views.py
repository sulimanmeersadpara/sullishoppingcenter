from django.shortcuts import render,HttpResponse,redirect
from .utils import send_email_to_client
from .forms import formValidations
from accounts.models import User
from django.contrib.auth import login,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout
from add_to_card.models import Card
from django.http import HttpRequest,request
from django.db.models import Sum
def signup(request):
    try:
        errors={}
        values={}
        if(request.method == "POST"):
            firstname=request.POST['firstname']
            email=request.POST['email']
            password=request.POST['password']
            confirm_password=request.POST['confirm_password']
            if(formValidations.is_valid_username(firstname)==False):
                errors.update({'username':'invalid username ,please enter only characters in user name'})
            if formValidations.is_valid_mail(email) == False:
                errors.update({'email':'please input a valid email'})
            if( formValidations.password_match(password,confirm_password) == False ):
                errors.update({'password':'passwords did not not match'})
       
            if(errors):
                values.update({'username':firstname})
                values.update({'email':email})
                values.update({'password':password})
                values.update({'errors':errors})
                return render(request,'accounts/singup.html',values)
            else:
            
                if not User.objects.filter(email=email).exists():
                    status,otp=send_email_to_client(email)
                    user = User(username=email, email=email,first_name=firstname,code=str(otp))
                    user.set_password(password)  # Hash the password
                    user.save()
                    return render(request,'accounts/verify.html',{'email':email})
                    
                    
                #---------------------dynamic path will come
                else:
                    errors.update({'email_exist':'this email is already exist'})
       
                values.update({'errors':errors})
                return render(request,'accounts/singup.html',values)
        
        return render(request,'accounts/singup.html')
    except Exception as e:
        messages.warning(request,"something went wrong")
        messages.warning(request,e)
        return render(request,'home/notPageFoundError.html')
        
        
        

    
        

def signin(request):
#    try:
        if request.method == "POST":
            username = request.POST['email']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
            # Log in the user and redirect to home
                if(user.is_verified == 0 and user.is_staff == 0):
                    messages.warning(request,'your account is not verified yet.we have sent a code to your email so enter that code to verify your account')
                    status,otp=send_email_to_client(username)
                    user.code=str(otp)
                    user.save()
                    return render(request,'accounts/verify.html',{'email':username})
                else:
                    login(request, user)
                    
                    total_qty = Card.objects.filter(c_user=request.user).aggregate(total=Sum('quantity'))['total']
                    request.session['NumberOfCartItems']=total_qty
                    messages.success(request, f"you have loggined successfully  {user.first_name}")
                    if 'path' in request.session:
                        return redirect(request.session['path'])
                    
            else:
                messages.warning(request,"you intered incorrect username password")
        return render(request,'accounts/signin.html')

 #   except Exception as e:
        messages.warning(request,"something went wrong")
        messages.warning(request,e)
        return render(request,'home/notPageFoundError.html')


@login_required
def logout_view(request):
    try:
        logout(request)
        
        messages.warning(request, "You have been logged out successfully.")
        request.session['NumberOfCartItems']=None
        previous_url = request.session.get('previous_url', '/')
        
        return redirect(previous_url)
    except Exception as e:
        messages.warning(request,"something went wrong")
        messages.warning(request,e)
        return render(request,'home/notPageFoundError.html')
