
from django.urls import path
from .views import orderslist
from .views2 import send_order_confirmation_email
from .views3 import order_def,view_order
from .views4 import decrease_stock
urlpatterns = [
    path('',orderslist,name='orderslist'),
    path('send_order_confirmation_email',send_order_confirmation_email,name='send_order_confirmation_email'),
    path('order',order_def,name='order'),
    path('view_order/<id>',view_order,name='view_order'),
    path('decrease_stock/<id>',decrease_stock,name='decrease_stock'),
]