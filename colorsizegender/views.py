from django.shortcuts import render,HttpResponse,redirect
from categories.models import gender
from products.models import ColorVariant,SizeVariant
from django.contrib import messages

def gendercolorsizelist(request):
    try:
        genders=gender.objects.all().order_by('g_name')
        colors=ColorVariant.objects.all().order_by('color_name')
        sizes=SizeVariant.objects.all().order_by('size_name')
        return render(request,'gendercolorsize/gendercolorsizelist.html',{'genders':genders,'colors':colors,'sizes':sizes})
    except Exception as e:
        messages.warning(request,"something went wrong")
        messages.warning(request,e)
        return render(request,'home/notPageFoundError.html')
def addcolor(request):
    try:
        if(request.method=='POST'):
            color_name=request.POST['color_name']
            color_code=request.POST['color_code']
            if(color_name is not ''):
                if not ColorVariant.objects.filter(color_code=color_code).exists():
                    if not ColorVariant.objects.filter(color_name=color_name).exists():
                        add_color_database=ColorVariant(color_name=color_name,color_code=color_code)
                        add_color_database.save()
                        messages.success(request,'new color added successfully')
                    else:
                        messages.warning(request,'the color names should not be same.')
                        return redirect('addcolor')
                else:
                    messages.warning(request,'this color is already is exist')
                    return redirect('addcolor')
            else:
                messages.warning(request,'the color name should not empty')
                return redirect('addcolor')
            return redirect('gendercolorsizelist')
        return render(request,'gendercolorsize/addcolor.html')
    except Exception as e:
        messages.warning(request,"something went wrong")
        messages.warning(request,e)
        return redirect('gendercolorsizelist')


   
def addsize(request):
    try:
        if request.method=="POST":
            size_name=request.POST['size_name']
            if not SizeVariant.objects.filter(size_name=size_name).exists():
                add_size_obj=SizeVariant(size_name=size_name)
                add_size_obj.save()
                messages.success(request,'new size added successfully')
            else:
                messages.warning(request,'this size is already exist')
                return redirect('addsize')
            return redirect('gendercolorsizelist')
        return render(request,'gendercolorsize/addsize.html')
    except Exception as e:
        messages.warning(request,"something went wrong")
        messages.warning(request,e)
        return render(request,'gendercolorsize/addsize.html')


def addgender(request):
    try:
        if request.method=="POST":
            gender_name=request.POST['gender_name']
            if not gender.objects.filter(g_name=gender_name).exists():
                add_gender_obj=gender(g_name=gender_name)
                add_gender_obj.save()
                messages.success(request,'new gender added successfully')
            else:
                messages.warning(request,'this gender is already exist')
                return redirect('addgender')
            return redirect('gendercolorsizelist')

        return render(request,'gendercolorsize/addgender.html')
    except Exception as e:
        messages.warning(request,"something went wrong")
        messages.warning(request,e)
        return render(request,'gendercolorsize/addgender.html')

def deletecolor(request,id):
    try:
        color_obj=ColorVariant.objects.get(id=id)
        
        if(color_obj.color_product_variant.exists()):
            messages.warning(request,'there are some products related to this color. so if you want to delete this color , first remove that products')
        

        else:
            messages.warning(request,'color deleted successfully')
            color_obj.delete()
        return redirect('gendercolorsizelist')
    except Exception as e:
        messages.warning(request,"something went wrong")
        messages.warning(request,e)
        return redirect('gendercolorsizelist')

def deletesize(request,id):
    try:
        size_obj=SizeVariant.objects.get(id=id)
        if(size_obj.size_product_variant.exists()):
            messages.warning(request,'there are some products related to this size. so if you want to delete this size , first remove that products')

        else:
            size_obj.delete()
            messages.warning(request,'size deleted successfully')
        return redirect('gendercolorsizelist')
    except Exception as e:
        messages.warning(request,"something went wrong")
        messages.warning(request,e)
        return redirect('gendercolorsizelist')
def deletegender(request,id):
    try:
        gender_obj=gender.objects.get(g_id=id)
        if(gender_obj.product_gender.exists()):
            messages.warning(request,'there are some products related to this gender. so if you want to delete this gender , first remove that products')
        else:

            messages.warning(request,'gender deleted successfully')
            gender_obj.delete()
        return redirect('gendercolorsizelist')
    except Exception as e:
        messages.warning(request,"something went wrong")
        messages.warning(request,e)
        return redirect('gendercolorsizelist')