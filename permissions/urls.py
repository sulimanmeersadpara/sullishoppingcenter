from django.urls import path
from .views import permissions,delete_permission
urlpatterns = [
    path('',permissions,name='permissions'),
    path('delete_permission/<perm_id>/<emp_id>',delete_permission,name='delete_permission'),
]