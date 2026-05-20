
from django.urls import path
from .views import signin,signup,logout_view
from .views2 import verify,forget_password_gmail_for_otp,forget_password_verify_code_page
from .views3 import forget_password_change_password

urlpatterns = [
    path('signin/',signin,name='siginin'),
    path('signup/',signup,name='signup'),
    path('verify/',verify,name='verify'),
    path('logout/',logout_view,name='logout'),
    path('forget_password_gmail_for_otp/',forget_password_gmail_for_otp,name='forget_password_gmail_for_otp'),
    path('forget_password_verify_code_page/',forget_password_verify_code_page,name='forget_password_verify_code_page'),
    path('forget_password_change_password/',forget_password_change_password,name='forget_password_change_password'),
    

]
