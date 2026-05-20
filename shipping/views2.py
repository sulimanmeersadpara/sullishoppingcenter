from django.shortcuts import redirect,render,HttpResponse
from add_to_card.models import Card
from .models import cities,shipping_areas,customer_shipping_location
from datetime import date
from django.contrib import messages
def customer_detail(request):
    try:
        try:
            customer_data_shipping_location=customer_shipping_location.objects.get(user=request.user)
            user_found=True
            
        except:
            user_found=False
            
        card_data=Card.objects.filter(c_user=request.user)
        total=0
        for c in card_data:
            total=total+c.price*c.quantity
        cities_list=cities.objects.all()
        shipping_areas_list=shipping_areas.objects.all()
        if(request.method=="POST"):
            city=request.POST['city']
            shipping_area_id=request.POST['shipping_area']
            phone_number=request.POST['phone_number']
            address1=request.POST['address1']
            address2=request.POST['address2']
            delivery_option=request.POST['delivery_option']
            if(delivery_option == 'now'):
                delivery_date=date.today()
                
            elif(delivery_option == 'later'):
                delivery_date=request.POST['delivery_date']
                
            else:
                return HttpResponse('please select atleast one delveiry option')
            
            # user_found=request.POST['user_found']
            shipping_area_obj=shipping_areas.objects.get(id=shipping_area_id)
            shipping_area_base_price=shipping_area_obj.base_charge
            shipping_area_item_price=shipping_area_obj.additional_item_charge
            card_obj=Card.objects.filter(c_user=request.user)
            total_product_price=0
            per_item_shipping_price=shipping_area_base_price
            for c_o in card_obj:
                total_product_price=total_product_price+c_o.price*c_o.quantity
                per_item_shipping_price=per_item_shipping_price+shipping_area_item_price*c_o.quantity
            
            total=total_product_price+per_item_shipping_price
            advance_pay=(total/100)*shipping_area_obj.advance_payment_percent
        
            
            if(user_found == True):
                
                customer_data_obj=customer_shipping_location.objects.get(user=request.user)
                customer_data_obj.phone_number=phone_number
                customer_data_obj.shipping_area_id=shipping_area_obj
                customer_data_obj.address1=address1
                customer_data_obj.address2=address2
                customer_data_obj.deleivery_charges=per_item_shipping_price
                customer_data_obj.product_price=total_product_price
                customer_data_obj.total=total
                customer_data_obj.advance_pay=advance_pay
                customer_data_obj.delevery_option=delivery_option
                customer_data_obj.date_ordered=delivery_date
                customer_data_obj.online_paid=0
                customer_data_obj.rest_for_delvery=total-advance_pay
                customer_data_obj.save()
                request.session['customer_shipping_id'] = customer_data_obj.id
            else:
                customer_shipping_location_save=customer_shipping_location(phone_number=phone_number,shipping_area_id=shipping_area_obj,address1=address1,address2=address2,user=request.user,deleivery_charges=per_item_shipping_price,product_price=total_product_price,total=total,advance_pay=advance_pay,delevery_option=delivery_option,date_ordered=delivery_date,rest_for_delvery=total-advance_pay)
                customer_shipping_location_save.save()
                request.session['customer_shipping_id'] = customer_shipping_location_save.id
            
            return redirect('paymentbutton')

            
        elif(request.GET.get('city_selected_value')):
            city_id=request.GET.get('city_selected_value')
            city=cities.objects.get(id=city_id)
            shipping_areas_list=shipping_areas.objects.filter(city=city)
            if user_found is True:
                return render(request,'shipping/customer_detail.html',{'user_found':user_found,'customer_data_shipping_location':customer_data_shipping_location,'card_data':card_data,'total':total,'cities':cities_list,'shipping_areas':shipping_areas_list,'city':city})
            else:
                return render(request,'shipping/customer_detail.html',{'user_found':user_found,'card_data':card_data,'total':total,'cities':cities_list,'shipping_areas':shipping_areas_list,'city':city})
            
        elif(request.GET.get('selected_area')):
            shipping_area_obj=shipping_areas.objects.get(id=int(request.GET.get('selected_area')))
            city_id=shipping_area_obj.city.id
            city=cities.objects.get(id=city_id)
            shipping_areas_list=shipping_areas.objects.filter(city=city)
            if user_found is True:
                return render(request,'shipping/customer_detail.html',{'user_found':user_found,'customer_data_shipping_location':customer_data_shipping_location,'card_data':card_data,'total':total,'cities':cities_list,'shipping_areas':shipping_areas_list,'city':city,'shipping_area_obj':shipping_area_obj})
            else:     
                return render(request,'shipping/customer_detail.html',{'user_found':user_found,'card_data':card_data,'total':total,'cities':cities_list,'shipping_areas':shipping_areas_list,'city':city,'shipping_area_obj':shipping_area_obj})
            
        else:
            if user_found is True:
                return render(request,'shipping/customer_detail.html',{'user_found':user_found,'customer_data_shipping_location':customer_data_shipping_location,'card_data':card_data,'total':total,'cities':cities_list,'shipping_areas':shipping_areas_list,})
            else:
                return render(request,'shipping/customer_detail.html',{'user_found':user_found,'card_data':card_data,'total':total,'cities':cities_list,'shipping_areas':shipping_areas_list,})
            

    except Exception as e:
        messages.warning(request,"something went wrong")
        messages.warning(request,e)
        return render(request,'home/notPageFoundError.html')