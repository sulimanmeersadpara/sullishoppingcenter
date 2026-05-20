
from django.urls import path
from .views import gendercolorsizelist,addcolor,addgender,addsize,deletecolor,deletesize,deletegender
urlpatterns = [
    path('',gendercolorsizelist,name='gendercolorsizelist'),
    path('addcolor',addcolor,name='addcolor'),
    path('addsize',addsize,name='addsize'),
    path('addgender',addgender,name='addgender'),
    path('deletecolor/<id>',deletecolor,name='deletecolor'),
    path('deletesize/<id>',deletesize,name='deletesize'),
    path('deletegender/<id>',deletegender,name='deletegender'),
]