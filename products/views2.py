import random 
from django.core.paginator import Paginator
from django.shortcuts import render,redirect
import string
from random import randrange
import os
from categories.models import parent_category,child_category,gender
from products.models import product,product_variant,ColorVariant,SizeVariant
from django.http import HttpRequest,HttpResponse
from django.contrib import messages
from django.shortcuts import get_object_or_404
from accounts.utils import has_permission
from django.contrib import messages
def generate_unique_filename(filename):
    try:
        r=int(randrange(100,150))
        r1=str(r*100000)
        random_string = ''.join(random.choices(string.ascii_letters+r1+string.digits, k=r))
        extension = os.path.splitext(filename)[1]  # Get the file extension
        return f"{random_string}{extension}"
    except Exception as e:
        return HttpRequest('sory something went wrong')
   
def get_products(request,slug):
    try:
        if request.GET.get('page'):
            page_number=request.GET.get('page') #this will come in url
        
        else:
            page_number='1'
        selected_size_list=[]
        selected_color_list=[]
        products_list=[]
        values={}
        child_categories_products=[]
        products_obj=product.objects.get(slug=slug)

        products=product_variant.objects.filter(product=products_obj).first()
        
        
        if( request.GET.get('status')=='size'):
                
                selected_size=request.GET.get('size')
                selected_color=request.GET.get('color')
                color=get_object_or_404(ColorVariant,color_name=selected_color)
                size=get_object_or_404(SizeVariant,size_name=selected_size)
                
                products_obj=product.objects.get(slug=slug)

                products=product_variant.objects.filter(product=products_obj,color=color,size=size).first()
        if( request.GET.get('status')=='color'):
                
                selected_color=request.GET.get('color')
                color=get_object_or_404(ColorVariant,color_name=selected_color)
                
                products_obj=product.objects.get(slug=slug)

                products=product_variant.objects.filter(product=products_obj,color=color).first()
        selected_color=products.color.color_name
        selected_size=products.size.size_name
        values.update({"product":products,'selected_color':selected_color,'selected_size':selected_size})
        
        # selected_price=None
        child_category_obj=products.product.p_child_category#it returned child category object of recored 1
        
        #related_products=product.objects.filter(p_child_category=child_category_obj)
        child_categories_products.append(child_category_obj)
        
        parent_category_obj=child_category_obj.p_category
        
        child_categories=child_category.objects.filter(p_category=parent_category_obj)
        product_gender=products.product.p_gender
        for i in child_categories:
            if(i.c_c_id is child_category_obj.c_c_id):
                pass
            else:
                child_categories_products.append(i)

        for child_category_item in child_categories_products:
            for productitem in child_category_item.p_child_category.all():
                
                if productitem.p_gender == product_gender:
                    products_list.append(productitem)

        paginator = Paginator(products_list, 16)
        ServiceDatafinal = paginator.get_page(page_number)
        totalpage=ServiceDatafinal.paginator.num_pages
        values.update({
            'page_no':int(page_number),
            'related_products':ServiceDatafinal,
            'lastpage':totalpage,
            'totalPagelist':[n+1 for n in range(totalpage)]
            })
        products_variants=product_variant.objects.filter(product=products_obj)
        product_color_obj=products.color
        
        for p_variants_size in products_variants :
            # if p_variants_size.size not in selected_size_list:
                # selected_size_list.append(p_variants_size.size)
            if p_variants_size.color == product_color_obj and p_variants_size.quantity > 0:
                 selected_size_list.append(p_variants_size.size)
            
        
    
        for p_variants_color in products_variants:
             if p_variants_color.color not in selected_color_list and p_variants_color.quantity > 0:
                  selected_color_list.append(p_variants_color.color)

        values.update({'selected_color_list':selected_color_list})
        values.update({'selected_color_list':selected_color_list,'selected_size_list':selected_size_list})
        # for color in products.color_variant.all() :
        
        #     selected_color=color.color_name
        #     if selected_color:
        #         break
        #normal_price=products.p_price
        
        # selected_color_price=products.get_product_price_by_color(selected_color)
        # selected_size_price=products.get_product_price_by_size(selected_size)
        # colors_charg=selected_color_price-normal_price
        # sizes_charg=selected_size_price-normal_price
        # price=normal_price+colors_charg+sizes_charg
       #values.update({'product':products,'selected_size':selected_size,'selected_color':selected_color,'selected_price':price})
        values.update({'product':products})
        
        
        
        categories=parent_category.objects.all()
        values.update({'categories':categories})
    #-----------------------------------------------------------------------------------

        request.session['path']=request.path
        
        values.update({'range_quantities': range(1, products.quantity+1)})
        
        return render(request,'products/products.html',values)
    except Exception as e:
        messages.warning(request,"something went wrong")
        messages.warning(request,e)
        return render(request,'home/notPageFoundError.html')
   
def product_list(request):
    try:
        if has_permission(request.user, 'add_product', 'products') or has_permission(request.user, 'view_product', 'products') or has_permission(request.user, 'delete_product', 'products') or has_permission(request.user, 'change_product', 'products'):
            if request.GET.get('page'):
                page_number=request.GET.get('page') #this will come in url
    
            else:
                page_number='1'

            values={}
            products=product.objects.all()
            # for p in products:
            #     variants = p.product_product_variant.all()
            #     for variant in variants:
            #         print(variant.size, variant.color, variant.price)
            # return HttpResponse('every thing done successfully')
            parent_categories=parent_category.objects.all()
            child_categories=child_category.objects.all()
            values.update({'parent_categories':parent_categories})
            values.update({'child_categories':child_categories})
            if(request.GET.get('slectedPcategoryId') and not request.GET.get('slectedCcategoryId')):
                
                p_category_id=request.GET.get('slectedPcategoryId')
                p_c_id=int(p_category_id)
                child_categories=child_category.objects.filter(p_category=p_category_id)
                l=[]
                for i in child_categories:
                    l.append(i.c_c_id)
                
                products=product.objects.filter(p_child_category__in = l)
                
                values.update({'child_categories':child_categories})
                values.update({'p_category_id':p_c_id})
                
                
            elif(request.GET.get('slectedCcategoryId') and request.GET.get('slectedPcategoryId')):
                
                
                c_category_id=request.GET.get('slectedCcategoryId')
                p_category_id=request.GET.get('slectedPcategoryId')
                p_c_id=int(p_category_id)
                c_c_id=int(c_category_id)
                if(p_c_id is -1):
                    child_category_obj=child_category.objects.get(c_c_id=c_c_id)
                    p_c_id=child_category_obj.p_category_id
                    
                values.update({'p_category_id':p_c_id})
                values.update({'c_category_id':c_c_id})
                products=product.objects.filter(p_child_category = c_c_id)
                
                child_categories=child_category.objects.filter(p_category = p_c_id)
                values.update({'child_categories':child_categories})
            else:     
                products=product.objects.all()
                
            p=Paginator(products,15) #every page will show 2 records
            
            ServiceDatafinal=p.get_page(page_number) #it will return the two records to display in page
            totalpage=ServiceDatafinal.paginator.num_pages #it will return how much pages can be create from compairing/dividing the number of records and number should display for one page
            values.update({
            'page_no':int(page_number),
            'products':ServiceDatafinal,
            'lastpage':totalpage,
            'totalPagelist':[n+1 for n in range(totalpage)]
            
            })
            return render(request,'products/productslist.html',values)
        else:
             return redirect('home')
    except Exception as e:
        messages.warning(request,"something went wrong")
        messages.warning(request,e)
        return render(request,'home/notPageFoundError.html')
   
