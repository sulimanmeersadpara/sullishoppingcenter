import os
from django.shortcuts import get_object_or_404
from django.http import HttpRequest,HttpResponse
from products.models import ColorVariant,SizeVariant,gender
from django.shortcuts import render,redirect
from products.models import product,product_image
from .forms import formValidations
from django.conf import settings
from .utils import delete_image_file
from django.contrib import messages
from .views5 import delete_variant
from categories.models import parent_category,child_category,gender
from accounts.utils import has_permission

def update_products(request,slug):
   try:
      if has_permission(request.user, 'change_product', 'products'):
         errors={}
         values={}
         parent_categories=parent_category.objects.all()
         products=product.objects.get(slug = slug)
         slectrId=products.p_child_category.p_category.p_c_id
         C_category=products.p_child_category.c_c_id
         child_ctgry=child_category.objects.filter(p_category=slectrId)
         if(request.GET.get('slectedcategoryId')):
            slectctgrId=request.GET.get('slectedcategoryId')
            child_ctgry=child_category.objects.filter(p_category=slectctgrId).all().order_by('c_c_name')
            slectrId=int(slectctgrId)
            if child_ctgry:
               C_category_obj=child_ctgry[0]
               C_category=C_category_obj.c_c_id
               
            
         product_name=products.p_name
         product_company=products.p_compony
         gendr=products.p_gender.g_id
         product_description=products.p_description
         slug=products.slug
         values.update({'product_name':product_name,'product_company':product_company,'gender':gendr,'product_description':product_description,'parent_categories':parent_categories,'child_ctgry':child_ctgry,'slug':slug})
         genders=gender.objects.all()
         values.update({'genders':genders})
         if(request.method == "POST"):
            
            c_cat=int(request.POST['product_child'])
            c_cat_instance=get_object_or_404(child_category,c_c_id=c_cat)
            
            product_name=request.POST["product_name"]
            product_company=request.POST["product_company"]
            product_description=request.POST["product_description"]
            Gender=request.POST['Gender']
            Gender1=int(Gender)
            gender_instance = get_object_or_404(gender,g_id=Gender1)
            #return HttpResponse(gender_instance)
            #------------------------validations------------------------------------
            
            product_name=request.POST["product_name"]
            if formValidations.is_valid_username(product_name):
               pass
            else:
               
               errors.update({"error_product_name":"invalid user name please use only characters and numbers only"})
            if formValidations.is_valid_username(product_company):
                  pass
            else:
                  errors.update({"error_company":"invalid name of company please use only characters and numbers only"})

            if(errors):
               values.update(errors)
               return render(request,'products/update_products.html',values)
            
            else:
               
               products=product.objects.get(slug=slug)
               products.p_name=product_name
               products.p_compony=product_company
               products.p_gender=gender_instance
               products.p_description=product_description
               products.p_child_category=c_cat_instance
               products.save()
               messages.success(request,'data updated successfully')
                  
               return redirect('manipulation')
      
         
         
         
         values.update({'slectrId':slectrId,'C_category':C_category,'child_ctgry':child_ctgry})
         
         return render(request,'products/update_products.html',values)
      else:
         return redirect('home')
         
   except Exception as e:
      messages.warning(request,"something went wrong")
      messages.warning(request,e)
      return redirect('home')

def delete_products(request,slug):
   try:
      if has_permission(request.user, 'delete_product', 'products'):
         record = get_object_or_404(product, slug=slug)
         products_varaints=record.product_product_variant.all()
         for p_variant in products_varaints:
            pv_id=int(p_variant.pv_id)
            delete_variant(request,pv_id)
         record.delete()
         messages.warning(request,'data deleted successfully')
         return redirect('manipulation')   
      else:
         return redirect('home')   
   except Exception as e:
        messages.warning(request,"something went wrong")
        messages.warning(request,e)
        return render(request,'home/notPageFoundError.html')
   
