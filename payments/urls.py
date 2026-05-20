from django.urls import path
from .views import paymentbutton
from .views2 import payment_response
urlpatterns = [
    path('paymentbutton/',paymentbutton,name='paymentbutton'),
    path('payment_response/',payment_response,name='payment_response')
    
    
]