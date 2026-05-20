from django.core.files.storage import FileSystemStorage
from .views2 import generate_unique_filename
from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from .models import product,product_image,product_variant,ColorVariant,SizeVariant
from django.contrib import messages
from .forms import formValidations
from .utils import delete_image_file
from accounts.utils import has_permission
def product_variants_menpulation(request,slug):
    try:    
        if has_permission(request.user, 'add_product', 'products') or has_permission(request.user, 'view_product', 'products') or has_permission(request.user, 'delete_product', 'products') or has_permission(request.user, 'change_product', 'products'):
            values={}
            p_obj=product.objects.get(slug=slug)
            products=product_variant.objects.filter(product=p_obj)
            values.update({'products':products,'slug':slug})
            #products
            return render(request,'products/products_menipulation_page.html',values)
        else:
             return redirect('home')
    except:
         messages.warning(request,'something went wrong')
def delete_variant(request , pv_id):
    try:
        if has_permission(request.user, 'delete_product', 'products'):
            image_names=[]
            record = get_object_or_404(product_variant, pv_id=pv_id)
            imagelist=product_image.objects.filter(product_variant_id=record)
            for image in imagelist:
                image_names.append(str(image.image))
            
            for image in image_names:
                #return HttpResponse(image)
                delete_image_file(image)
                # Deletes the file from media folder
                
            record.delete()
        else:
            return redirect('home')
    except Exception as e:
        messages.warning(request,"something went wrong")
        messages.warning(request,e)
        return render(request,'home/notPageFoundError.html')
   
            
def delete_variantFunc(request, slug , pv_id):
    try:
        if has_permission(request.user, 'delete_product', 'products'):

            delete_variant(request , pv_id)
            
            record = get_object_or_404(product, slug=slug)
            products_varaints=record.product_product_variant.all()
            if products_varaints:
                
                messages.warning(request,'product variant deleted successfully')
                return redirect('product_variants_menpulation',slug=slug) 
            else:
                
                messages.warning(request,'product deleted successfully')
                record.delete()
                return redirect('manipulation') 
        else:
            return redirect('home')
    except Exception as e:
        messages.warning(request,"something went wrong")
        messages.warning(request,e)
        return render(request,'home/notPageFoundError.html')
   
                #delete_products(request,slug)
def add_new_variant(request,slug):
    try:
        if has_permission(request.user, 'add_product', 'products'):

            values={}
            errors={}
            products=product.objects.get(slug=slug)
            if request.method=="POST":
                product_size=int(request.POST['product_sizes'])
                product_color=int(request.POST['product_colors'])
                product_price=request.POST['product_price']
                product_quantity=request.POST['product_quantity']
                size_instant=get_object_or_404(SizeVariant,id=product_size)
                color_instant=get_object_or_404(ColorVariant,id=product_color)      
                
                if request.POST.get('is_sale_checkbox') == 'on':
                    is_sale_checkbox=1
                    product_sale_price=request.POST['product_sale_price']
                else:
                    is_sale_checkbox=0
                    product_sale_price=0
                images = request.FILES.getlist('image')
                if not images:
                        errors.update({'images_empty':'please upload atleast one picture of the product'})
                for i in images:
                        is_image_valid = formValidations.is_valid_image(i.name)
                        if is_image_valid == 0:
                            errors.update({"image":"invalid formate of images please make sure that all images either be jpg,jpeg,or png"})
                product_variantobj=product_variant(product=products,size=size_instant,color=color_instant,price=product_price,quantity=product_quantity,is_available=1,p_is_sale=is_sale_checkbox,sale_price=product_sale_price)
                product_variantobj.save()    
                
                for j in images:
                    new_name = generate_unique_filename(j.name)
                    fs = FileSystemStorage()
                    filename = fs.save(new_name, j)
                    
                    product_image.objects.create(product_id=products,product_variant_id=product_variantobj,image=filename)
                    
                    
                return redirect('product_variants_menpulation',slug=slug)
            sizes=SizeVariant.objects.all()
            colors=ColorVariant.objects.all()
            
            values.update({'sizes':sizes,'colors':colors,'products':products})
            return render(request,'products/add_new_variant.html',values)
        else:
            return redirect('home')
    except Exception as e:
        messages.warning(request,"something went wrong")
        messages.warning(request,e)
        return render(request,'home/notPageFoundError.html')
   