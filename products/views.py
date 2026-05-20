from django.shortcuts import render,HttpResponseRedirect,redirect
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponse
from categories.models import parent_category,child_category,gender
from .models import product,ColorVariant,SizeVariant,product_image,product_variant
from .forms import formValidations
from django.core.files.storage import FileSystemStorage
from django.utils.text import slugify #it creates slugs automatically
from django.shortcuts import get_object_or_404
from random import randrange
from django.conf import settings 
import string
import random
import os
from .views2 import generate_unique_filename
from accounts.utils import has_permission

# Create your views here.

def add_products(request):
    try:
        if has_permission(request.user, 'add_product', 'products'):
            values={}
            int_colors=[]
            int_sizes=[]
            colorlist=[]
            chctry=-1
            obj=''
            parent_category_obj=parent_category.objects.first()
            #parent_category_obj=parent_category.objects.all()[0]
            if(parent_category_obj is not None):
                parent_categories_id=parent_category_obj.p_c_id
            
                obj=child_category.objects.filter(p_category=parent_categories_id).all()
                    
            colors=ColorVariant.objects.all().order_by('color_name')
            sizes=SizeVariant.objects.all().order_by('size_name')
            #return HttpResponse(colors)
            color_size=product_variant.objects.all()
            slectctgrId=request.GET.get('slectedcategoryId')
            if(slectctgrId):
                chctry=slectctgrId
                chctry=int(chctry)
            genders=gender.objects.all()
            values.update({'genders':genders})
             #--_____|_______-------|-------________|________------|------__________|___________------------|---------_______|___________-----------------
            if(request.method=="POST"):
                errors={}
                images = request.FILES.getlist('image') 
                is_sale_checkbox=request.POST.getlist('is_sale_checkbox')
                
                int_is_sale_checkbox=[int(i) for i in is_sale_checkbox]
                is_sale_checkbox=int_is_sale_checkbox
                
                product_sale_price=request.POST.getlist('product_sale_price')
                
                int_product_sale_price=[int(i) for i in product_sale_price]
                product_sale_price=int_product_sale_price
                
                image_products_variants = request.POST.getlist('product_variant_number')
                int_image_products_variants=[int(i) for i in image_products_variants]
                image_products_variants=int_image_products_variants
                
                
                P_category=request.POST['product_parent_category']#it returns id of subject
                P_category=int(P_category)
                C_category=request.POST['product_child']
                C_category=int(C_category)
                product_name=request.POST["product_name"]
                
                total_product_variants=int(request.POST['total_product_variants'])
                
                if formValidations.is_valid_username(product_name):
                    pass
                else:
                
                    errors.update({"product_name":"invalid user name please use only characters and numbers only"})
                
                #------------------------------------------------------------------------
                product_price=request.POST.getlist("product_price")
                int_prices=[int(i) for i in product_price]
                product_price=int_prices
                
                for p_price in product_price:   
                    if formValidations.is_valid_price(p_price):
                        pass
                    else:
                        errors.update({"price":"invalid price , please input a valid price an integer or a float"})
                product_quantity=request.POST.getlist('product_quantity')
                int_quantity=[int(i) for i in product_quantity]
                product_quantity=int_quantity
                
                #return HttpResponse(k)
                #--------------------------------------------------------------
                product_company=request.POST["product_company"]
                if formValidations.is_valid_username(product_company):
                    pass
                else:
                    errors.update({"company":"invalid name of company please use only characters and numbers only"})
                
                #--------------------------------------------------------------
                product_description =request.POST["product_description"]
                #--------------------------------------------------------------
                Gender=request.POST["Gender"]
                Gender1=int(Gender)
                #--------------------------------------------------------------
                product_color=request.POST.getlist("product_colors")
                #return HttpResponse(product_color)
                int_colors=[int(i) for i in product_color]
                if not int_colors:
                    errors.update({'colors':'please select atleast one color'})
                
            
                #--------------------------------------------------------------
                product_size=request.POST.getlist("product_sizes")
                
                int_sizes=[int(i) for i in product_size]
                if not int_sizes:
                    errors.update({'sizes':'please select atleast one size'})
                #------------------------------------
                if not images:
                    errors.update({'images_empty':'please upload atleast one picture of the product'})
                #--------------------------------------------------------------
                l=[]
                for i in images:
                    is_image_valid = formValidations.is_valid_image(i.name)
                    if is_image_valid == 0:
                        errors.update({"image":"invalid formate of images please make sure that all images either be jpg,jpeg,or png"})
                parent_categories = parent_category.objects.all()
                
                c_ctr=int(C_category)
                child_categories=child_category.objects.filter(p_category=P_category).all()  
                random_number = randrange(10000000000, 99999999999)  # Random odd number between 1 and 9
                random_number=str(random_number)
                slug=product_name+'-'+random_number+'-'+product_company 
                slug=slugify(slug)
                min_price=product_price[0]
                max_price=product_price[0]
                for p in product_price:
                    if(p<min_price):
                        min_price=p
                    if(p>max_price):
                        max_price=p
                for p in product_sale_price:
                    if p<min_price and p is not 0:
                        min_price=p
                
                if(errors):
                    values.update({'child_ctgry':child_categories,'parent_categories':parent_categories,'product_name':product_name,'product_price':product_price,'product_company':product_company,'product_description':product_description,'gender':Gender1,'slectrId':P_category,'C_category':c_ctr,'error':errors,'colors':colors,'sizes':sizes,'int_colors':int_colors,'int_sizes':int_sizes})   

                    return render(request,'products/add_products.html',values)#if form validation errors occurs then to show errors in template files
                else:
                    data=child_category.objects.get(c_c_id=c_ctr)
                    
                    category_instance = get_object_or_404(child_category, c_c_id=c_ctr)
                    gender_instance= get_object_or_404(gender,g_id=Gender1)
                    add_products_database=product(p_name=product_name,p_compony=product_company,p_description=product_description,p_child_category=category_instance,min_price=min_price,max_price=max_price,p_gender=gender_instance,slug=slug)
                    add_products_database.save()
                    
                    #-----------------------------------------------------------------------for images------------------------------

                
                    product_instance= get_object_or_404(product,p_id=add_products_database.p_id)
                    check_box_var=0
                    
                    for i in range(total_product_variants):
                        color_instant=get_object_or_404(ColorVariant,id=int_colors[i])
                        size_instant=get_object_or_404(SizeVariant,id=int_sizes[i])
                        product_variantobj=product_variant(product=product_instance,size=size_instant,color=color_instant,price=product_price[i],quantity=product_quantity[i],is_available=1)
                        if len(is_sale_checkbox)<=0:
                            product_variantobj.p_is_sale=0
                            product_variantobj.sale_price=0
                        else:
                            if check_box_var<len(is_sale_checkbox):
                                if i+1 == is_sale_checkbox[check_box_var]:
                                    product_variantobj.p_is_sale=1
                                    product_variantobj.sale_price=product_sale_price[i]
                                    check_box_var=check_box_var+1
                                else:
                                    product_variantobj.p_is_sale=0
                                    product_variantobj.sale_price=0
                        product_variantobj.save()
                        product_variant_instant=get_object_or_404(product_variant,pv_id=product_variantobj.pv_id)
                        image_var=0
                        for j in image_products_variants:
                            if j == i+1:
                
                                uploaded_image=images[image_var]
                                new_name = generate_unique_filename(uploaded_image.name)
                                fs = FileSystemStorage()
                                filename = fs.save(new_name, uploaded_image)
                                imagesave=product_image.objects.create(product_id=product_instance,product_variant_id=product_variant_instant,image=filename)
                                imagesave.save()
                                image_var=image_var+1
                            else:
                                image_var=image_var+1

                                    

                    messages.success(request,'data saved successfully')
                    
                    total_products=product.objects.count()
                    product_page=15
                    totalpage=(total_products+product_page-1)//product_page
                    
                
                    return redirect(reverse('manipulation')+f'?page={str(totalpage)}')
                    
                    
                    
                    
            else:
                parent_categories = parent_category.objects.all().order_by('p_c_name')
                if(request.GET.get('slectedcategoryId')):
                    
                    slectctgrId=request.GET.get('slectedcategoryId')
                    if(slectctgrId == None):
                        
                        obj=child_category.objects.all().order_by('c_c_name')
                    #return HttpResponse(slectctgrId)
                    else:
                        obj=child_category.objects.filter(p_category=slectctgrId).all().order_by('c_c_name')
                
                    #data = employes.objects.get(id=id)
                #return HttpResponse(parent_categories)
                    
                values.update({'parent_categories':parent_categories,'child_ctgry':obj,'slectrId':chctry,'colors':colors,'sizes':sizes,'colorlist':colorlist,'int_sizes':int_sizes,'int_colors':int_colors})
                return render(request,'products/add_products.html',values)
        else:
            return redirect('home')
    except Exception as e:
        messages.warning(request,"something went wrong")
        messages.warning(request,e)
        return render(request,'home/notPageFoundError.html')
   

