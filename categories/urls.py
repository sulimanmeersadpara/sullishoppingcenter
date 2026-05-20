
from django.contrib import admin
from django.urls import path
from .views import category_data
from .views1 import category_list,addchildcategory,addparentcategory,update_parent_category,update_child_category,delete_child_category,delete_parent_category
urlpatterns = [

    path('categories/category_data/<int:id>',category_data,name='category_data'),
    path('categories_menipulations',category_list,name='category_list'),  
    path('addchildcategory',addchildcategory,name='addchildcategory'),
    path('addparentcategory',addparentcategory,name='addparentcategory'),
    path('update_parent_category/<id>',update_parent_category,name='update_parent_category'),
    path('update_child_category/<id>',update_child_category,name='update_child_category'),
    path('delete_child_category/<id>',delete_child_category,name='delete_child_category'),
    path('delete_parent_category/<id>',delete_parent_category,name='delete_parent_category'),
 
    

]
