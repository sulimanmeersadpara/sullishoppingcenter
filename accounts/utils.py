from django.contrib.auth.models import User
import time
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpRequest,request
from django.shortcuts import render,HttpResponse
from django.conf import settings
import random
def send_email_to_client(email):
    try:

        otp = str(random.randint(100000, 999999))
        subject="🔒 Your One-Time Password (OTP) - Sulli Shopping Center"
        message=f"""
Dear Valued Customer,

Thank you for using Sulli Shopping Center.

Your One-Time Password (OTP) for verification is: {otp}

Please use this code as soon as posible to complete your verification.

If you didn’t request this code, please ignore this email.

Best regards,
Sulli Shopping Center
"""
        from_email= settings.EMAIL_HOST_USER
        if(send_mail(subject,message,from_email,[email])):
            return 1,int(otp)
        else:
            return 0,0
    except:
        return 0,0
# utils.py
def has_permission(user, perm_codename, app_label):
    if user.is_superuser:
        return True
    full_perm = f"{app_label}.{perm_codename}"
    return user.has_perm(full_perm)