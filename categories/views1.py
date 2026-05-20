from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from categories.models import child_category,parent_category
from products.models import product
from django.contrib import messages
from accounts.utils import has_permission
def category_list(request):
    try:
        
        if has_permission(request.user, 'add_parent_category', 'categories') or has_permission(request.user, 'change_parent_category', 'categories') or has_permission(request.user, 'delete_parent_category', 'categories') or has_permission(request.user, 'view_parent_category', 'categories') or has_permission(request.user, 'add_child_category', 'categories') or has_permission(request.user, 'change_child_category', 'categories') or has_permission(request.user, 'delete_child_category', 'categories') or has_permission(request.user, 'view_child_category', 'categories') :
            values={}
            p_categories=parent_category.objects.all()
            c_categories=child_category.objects.all()
            values.update({'p_categories':p_categories,'c_categories':c_categories})
            return render(request,'categories/category_list.html',values)
        else:
            return redirect('home')
    except:
        messages.warning(request,'something went wrong')
        return redirect('home')
def addparentcategory(request):
    try:
        if has_permission(request.user, 'add_parent_category', 'categories'):
            if(request.method=="POST"):
                p_category=request.POST['p_category']
                if(parent_category.objects.filter(p_c_name=p_category).exists()):
                    messages.warning(request,'this parent category is already exist')
                else:
                    parent_obj=parent_category(p_c_name=p_category)
                    parent_obj.save()
                    messages.success(request,"the parent category is add successfully")
                return redirect('category_list')
            else:
                return redirect('home')
        else:
            return redirect('home')
    except:
        messages.warning(request,'something went wrong')
        return redirect('home')
def addchildcategory(request):
    try:
        if has_permission(request.user, 'add_child_category', 'categories'):    
            if(request.method=="POST"):
                errors={}
                c_category=request.POST['c_category']
                parent_category_id=int(request.POST['parent_category'])
                try:
                    parent_category_object=get_object_or_404(parent_category,p_c_id=parent_category_id)
                    if(child_category.objects.filter(c_c_name=c_category,p_category=parent_category_object).exists()):
                        messages.warning(request,'this child category is already exist')
                        
                    else:
                        child_category_obj=child_category(c_c_name=c_category,p_category=parent_category_object)
                        child_category_obj.save()
                        messages.success(request,'the child category is added successfully')
                    return redirect('category_list')
                except:
                    errors.update({'parent_category':'this parent category is not found'})
                return HttpResponse(parent_category_object)
            else:
                return redirect('home')
    except:
        messages.warning(request,'something went wrong')
        return redirect('home')        
def update_parent_category(request,id):
    try:
        if has_permission(request.user, 'change_parent_category', 'categories'):
            values={}
            parent_category_obj=get_object_or_404(parent_category,p_c_id=id)
            
            if(request.method=="POST"):
                
                p_category=request.POST['p_category']
            
                
                if(parent_category.objects.filter(p_c_name=p_category).exists()):
                    messages.warning(request,'this parent category is already exist')
                else:
                    parent_category_obj.p_c_name=p_category
                    parent_category_obj.save()
                    messages.success(request,'the parent category updated successfully')
                    return redirect('category_list')

            

            values.update({'parent_category':parent_category_obj})
            return render(request,'categories/update_parent_category.html',values)

        else:
            return redirect('home')    
    except Exception as e:
        messages.warning(request,"something went wrong")
        messages.warning(request,e)
        return render(request,'home/notPageFoundError.html')
        
def delete_parent_category(request,id):
    try:
        if has_permission(request.user, 'delete_parent_category', 'categories'):
            parent_category_obj=get_object_or_404(parent_category,p_c_id=id)
            child_category_objects=child_category.objects.filter(p_category=parent_category_obj)
            status=0
            for child_category_obj in child_category_objects:
                if(product.objects.filter(p_child_category=child_category_obj).exists()):
                    messages.warning(request,"a child category of this parent category is related to some existing products, so if you want to remove this parent category , please first delete the products which are related to any child category of this parent category ")
                    status=1
                    break
            if(status is 0):
                parent_category_obj.delete()
                messages.warning(request,'the parent category is deleted successfully')
            return redirect('category_list')
        else:
            return redirect('home')
    except:
        messages.warning(request,'something went wrong')   
def update_child_category(request,id):
    try:
        if has_permission(request.user, 'change_child_category', 'categories'):
            values={}
            child_category_obj=get_object_or_404(child_category,c_c_id=id)
            if(request.method=="POST"):
                c_category=request.POST['child_category']

                p_category_id=int(request.POST['parent_category'])
                try:
                    parent_category_obj=get_object_or_404(parent_category,p_c_id=p_category_id)
                    if(child_category.objects.filter(c_c_name=c_category,p_category=parent_category_obj).exists()):
                        messages.warning(request,'this child category is already exist')
                    else:
                        child_category_obj.c_c_name=c_category
                        child_category_obj.p_category=parent_category_obj
                        child_category_obj.save()
                        messages.success(request,'the child category updated successfully')
                        return redirect('category_list')

                except:
                    messages.warning(request,'the parent category is not found')

            parent_categories=parent_category.objects.all()
            values.update({'child_category':child_category_obj,'parent_categories':parent_categories})
            return render(request,'categories/update_child_category.html',values)
        else:
            return redirect('home')    
    except:
        messages.warning(request,'this child category is not found')
        return redirect('category_list')
def delete_child_category(request,id):
    try:
        if has_permission(request.user, 'delete_child_category', 'categories'):
            child_category_obj=get_object_or_404(child_category,c_c_id=id)
            if(product.objects.filter(p_child_category=child_category_obj).exists()):
                messages.warning(request,'this child category already belongs to some products, so if you want to delete this category , first delete that products')
            else:
                child_category_obj.delete()
                messages.warning(request,'the category deleted successfully')
        else:
            return redirect('home')       
    except:
        messages.warning(request,'this child category is not found')
    return redirect('category_list')

    
