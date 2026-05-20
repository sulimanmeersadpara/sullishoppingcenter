from django.shortcuts import render,HttpResponse,redirect
from add_to_card.models import Card
from accounts.models import User
from shipping.models import shipping_areas,customer_shipping_location
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login
from accounts.models import User

@csrf_exempt
def payment_response(request):
        
        data = request.POST.dict()   # get all JazzCash returned values
        # You can access any value like this:
        response_code   = int(data.get("pp_ResponseCode"))
        
        ppmpf_1 = data.get('ppmpf_1')
        ppmpf_2 = data.get('ppmpf_2')
        
        amount          = data.get("pp_Amount")
        user=User.objects.get(id=ppmpf_1)
        request.session['NumberOfCartItems']=ppmpf_2
        card_data=Card.objects.filter(c_user=user)
        
        user_obj=User.objects.get(id=user.id)
        login(request, user_obj)
        customerse_place_obj=customer_shipping_location.objects.get(user=user)
        
        if response_code == 199:
                msg = f"✅Payment of {amount} has been successfully received. The remaining balance will be collected upon delivery."
                
                messages.success(request,msg)
                customerse_place_obj.online_paid=customerse_place_obj.online_paid+int(amount)
                customerse_place_obj.save()
                return redirect('order')
        else:
                messages.warning(request,"⚠️transaction failed please try again")
        
        context={'card_data':card_data,'customerse_place_obj':customerse_place_obj}
        return render(request,'payments/paymentbutton.html',context)
        