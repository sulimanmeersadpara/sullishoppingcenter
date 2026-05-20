from django.shortcuts import render,HttpResponse,redirect
from products.models import product_variant,SizeVariant,ColorVariant
from django.shortcuts import get_object_or_404
from django.contrib import messages
from accounts.utils import has_permission
def product_variant_update(request,pv_id):
    try:
        if has_permission(request.user, 'change_product', 'products'):  
            values={}
            
            products=product_variant.objects.get(pv_id=pv_id)
            if request.method == "POST":
                product_size=int(request.POST['product_sizes'])
                product_color=int(request.POST['product_colors'])
                product_price=int(request.POST['product_price'])
                product_quantity=request.POST['product_quantity']
                size_instant=get_object_or_404(SizeVariant,id=product_size)
                color_instant=get_object_or_404(ColorVariant,id=product_color)
                products.size=size_instant
                products.color=color_instant
                products.price=product_price
                products.quantity=product_quantity
                if request.POST.get('is_sale_checkbox') == 'on':
                    is_sale_checkbox=1
                    product_sale_price=int(request.POST['product_sale_price'])
                else:
                    is_sale_checkbox=0
                    product_sale_price=0
                
                products.p_is_sale=is_sale_checkbox
                products.sale_price=product_sale_price
                products.save()
                product_obj=products.product
                products=product_variant.objects.filter(product=product_obj)
                if(is_sale_checkbox == 1):
                    min_price=product_sale_price
                    
                else:
                    min_price=product_price
                max_price=product_price
                for i in products:
                    
                    if(i.price < min_price):

                        min_price=i.price
                    if(i.price>max_price):
                        max_price=i.price
                
                product_obj.min_price=min_price
                product_obj.max_price=max_price
                product_obj.save() 
                messages.success(request,'data updated successfully')
                slug=product_obj.slug
                return redirect('product_variants_menpulation',slug=slug)
            sizes=SizeVariant.objects.all()
            colors=ColorVariant.objects.all().order_by('color_name')
            values.update({'sizes':sizes,'colors':colors,'products':products})
        
            return render(request,'products/product_variant_update.html',values)
        else:
            return redirect('home')
    except Exception as e:
        messages.warning(request,"something went wrong")
        messages.warning(request,e)
        return render(request,'home/notPageFoundError.html')
   

