from django.core.mail import send_mail
from django.conf import settings
import random
from django.shortcuts import HttpResponse
def has_permission_for_dashboard(user):
    if user.is_superuser:  
        return True
    elif user.is_staff:
        return True
    else:
        return False

def sendmail():
    try:
        otp = str(random.randint(100000, 999999))
        subject="OTP"
        message="Your otp is number is "+otp
        from_email= settings.EMAIL_HOST_USER
        recipient_list=['sulligabbar@gmail.com']
        
        if(send_mail(subject,message,from_email,recipient_list)):
            return 1,int(otp)
        else:
            return 0
    except:
        return 0

        