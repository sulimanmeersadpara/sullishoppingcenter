from django.core.files.storage import FileSystemStorage
from .views2 import generate_unique_filename
from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from .models import product,product_image,product_variant
from django.contrib import messages
from .utils import delete_image_file
import os

from accounts.utils import has_permission
def images(request,slug,pv_id):
    try:
        if has_permission(request.user, 'add_product', 'products') or has_permission(request.user, 'delete_product', 'products') or has_permission(request.user, 'change_product', 'products') or has_permission(request.user, 'view_product', 'products'):
            if request.method == "POST":
                renamad_images=[]
            
                images=request.FILES.getlist('image')
                if not images:
                    messages.warning(request,"please input atleast one image")
                    return redirect("images",slug=slug)

                
                product_instance= get_object_or_404(product,slug=slug)
                
                product_variant_instance=get_object_or_404(product_variant,pv_id=int(pv_id))
                

                for uploaded_image in images:
                    new_name = generate_unique_filename(uploaded_image.name)
                    fs = FileSystemStorage()
                    filename = fs.save(new_name, uploaded_image)
                    # Store the file path (URL) or ImageField instance for saving in the model
                    renamad_images.append(filename)

                    #return HttpResponse(renamad_images)

                for image_file in renamad_images:
                    product_image.objects.create(product_id=product_instance,image=image_file,product_variant_id=product_variant_instance)

                messages.success(request,"image uploaded successfully")                
                new_slug=slug
                new_pv_id=pv_id
                return redirect("images",slug=new_slug,pv_id=new_pv_id)
            values={}
            products=product_variant.objects.get(pv_id=pv_id)
            values.update({'products':products})
            return render(request,'products/images.html',values)
        else:
            return redirect('home')
    except Exception as e:
        messages.warning(request,"something went wrong")
        messages.warning(request,e)
        return render(request,'home/notPageFoundError.html')
   
def delete_images(request, id):
    try:
        if(has_permission(request.user, 'delete_product', 'products')):    
            image = get_object_or_404(product_image, i_id=id)
            slug = image.product_id.slug
            new_pv_id = image.product_variant_id.pv_id

            # Delete the image file from storage
            image.image.delete(save=False)

            # Delete the DB record
            image.delete()

            messages.warning(request, "Image deleted successfully")
            return redirect("images", slug=slug, pv_id=new_pv_id)

        else:
            return redirect('home')

    except Exception as e:
        messages.warning(request, "Something went wrong")
        return redirect('home')
      