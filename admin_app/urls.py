
from django.urls import path
from . import views,views2,views3
#from .views import custom_404_view  # Import from wherever you placed it

#handler404 = custom_404_view
urlpatterns = [
    path('', views.admin_auth_page),
    path('emailforcode', views2.emailforcode,name='emailforcode'),
    path('sixdigitcodesubmit/<str:email>/', views2.sixdigitcodesubmit,name='sixdigitcodesubmit'),
    path('dashboard/', views3.dashboard,name='dashboard'),
   
]