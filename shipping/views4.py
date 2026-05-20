from django.shortcuts import redirect,render,HttpResponse
from .models import country,cities
from django.contrib import messages

def cities_country_list(request):
    try:
        if request.method=='POST':
            form_type = request.POST.get('form_type')
            
            if(form_type == 'country_form'):
                country_name=request.POST['country']
                add_country=country(country_name=country_name)
                add_country.save()
            elif(form_type == 'city_form'):
                city_name=request.POST['city']
                if(cities.objects.filter(city_name=city_name).exists()):
                    return HttpResponse('the city is already found')
                else:
                    add_city=cities(city_name=city_name)
                    add_city.save()
                    messages.success(request,'new city added successfully')
                    return redirect('cities_country_list')
        cities_list=cities.objects.all()
        country_name=country.objects.first()
        return render(request,'shipping/cities_country_list.html',{'cities':cities_list,'country':country_name})
    except Exception as e:
        messages.warning(request,"something went wrong")
        messages.warning(request,e)
        return render(request,'home/notPageFoundError.html')
def delete_cities(request,id):
    try:
        city=cities.objects.get(id=id)
        city.delete()
        messages.warning(request,'the city deleted successfully')
        return redirect('cities_country_list')
    except Exception as e:
        messages.warning(request,"something went wrong")
        messages.warning(request,e)
        return render(request,'home/notPageFoundError.html')
def delete_countries(request,id):
    try:
        country_obj=country.objects.get(id=id)
        country_obj.delete()
        messages.warning(request,'the country deleted successfully')
        return redirect('cities_country_list')
    except Exception as e:
        messages.warning(request,"something went wrong")
        messages.warning(request,e)
        return render(request,'home/notPageFoundError.html')
def update_cities(request,id):
    try:
        city=cities.objects.get(id=id)
        if request.method=='POST':
            city_name=request.POST['city']
            city.city_name=city_name
            city.save()
            messages.success(request,'the city updated successfully')
            return redirect('cities_country_list')
        return render(request,'shipping/update_cities.html',{'city':city})
    except Exception as e:
        messages.warning(request,"something went wrong")
        messages.warning(request,e)
        return render(request,'home/notPageFoundError.html')
def update_countries(request,id):
    try:
        country_obj=country.objects.get(id=id)
        if request.method=='POST':
            country_name=request.POST['country']
            country_obj.country_name=country_name
            country_obj.save()
            messages.success(request,'the country updated successfully')
            return redirect('cities_country_list')
        return render(request,'shipping/update_countries.html',{'country':country_obj})
    except Exception as e:
        messages.warning(request,"something went wrong")
        messages.warning(request,e)
        return render(request,'home/notPageFoundError.html')