from django.urls import path
from .views2 import success_checkout
from .views3 import history

urlpatterns = [
    path('success_checkout',success_checkout,name='success_checkout'),
    path('history/<id>',history,name='history'),
    
]