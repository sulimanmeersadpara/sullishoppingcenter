

from django.urls import path
from .views import add_employee,employee_list
from .views3 import delete_employee,update_employee
from .view4 import change_profile_image,employee_account,change_password

urlpatterns = [
    
    path('add_employee/',add_employee,name='add_employee'),
    path('employee_list/',employee_list,name='employee_list'),
    path('delete_employee/<id>',delete_employee,name='delete_employee'),
    path('update_employee/<id>',update_employee,name='update_employee'),
    path('employee_account',employee_account,name='employee_account'),
    path('change_profile_image',change_profile_image,name='change_profile_image'),
    path('change_password',change_password,name='change_password'),
]