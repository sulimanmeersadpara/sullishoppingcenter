from django.urls import path,include
from .views import shipping_menipulations
from .views2 import customer_detail
from .views3 import add_shipping_areas,delete_shipping,update_shipping
from .views4 import cities_country_list,delete_cities,update_cities,update_countries,delete_countries
urlpatterns = [
    path('',shipping_menipulations,name='shipping_menipulations'),
    path('delete_shipping/<id>',delete_shipping,name='delete_shipping'),
    path('update_shipping/<id>',update_shipping,name='update_shipping'),
    path('customer_detail',customer_detail,name='customer_detail'),
    path('add_shipping_areas',add_shipping_areas,name='add_shipping_areas'),
    path('cities_country_list',cities_country_list,name='cities_country_list'),
    path('delete_cities/<id>',delete_cities,name='delete_cities'),
    path('update_cities/<id>',update_cities,name='update_cities'),
    path('delete_countries/<id>',delete_countries,name='delete_countries'),
    path('update_countries/<id>',update_countries,name='update_countries')
    
]
