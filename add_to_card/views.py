from django.shortcuts import render,HttpResponse,redirect,HttpResponseRedirect
from products.models import product,product_variant
from .models import Card
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.db.models import Sum
def cart(request):
    try:
        values={}
        if(request.GET.get('decreaseQuantity')):
            id=request.GET.get('decreaseQuantity')
            cartObj=Card.objects.get(c_id=id)
            if cartObj.quantity>1:
                cartObj.quantity=cartObj.quantity-1
                cartObj.save()
                request.session['NumberOfCartItems']=request.session['NumberOfCartItems']-1
            return redirect('AtToCard') 
            
        if(request.GET.get('increaseQuantity')):
            id=request.GET.get('increaseQuantity')
            cartObj=Card.objects.get(c_id=id)
            cartObj.quantity=cartObj.quantity+1
            cartObj.save()
            request.session['NumberOfCartItems']=request.session['NumberOfCartItems']+1
            return redirect('AtToCard') 
        
        if(request.method == "POST"):
            if(request.user.id):
                if 'NumberOfCartItems' in request.session:
                    total_qty = Card.objects.filter(c_user=request.user).aggregate(total=Sum('quantity'))['total']
                    if(total_qty):
                        request.session['NumberOfCartItems']=int(total_qty)
                    else:
                        request.session['NumberOfCartItems']=0
                else:
                    request.session['NumberOfCartItems']=0
                p_v_id=int(request.POST['product_variant'])
                product_variant_obj=product_variant.objects.get(pv_id=p_v_id)
                
                slug=request.POST['slug']
                quantity=int(request.POST['quantity'])
                product_obj=product.objects.get(slug=slug)
                #user_obj is instance of user table and request.user is also instance
                if(Card.objects.filter(c_product_variant=product_variant_obj,c_user=request.user,c_product=product_obj).exists()):
                    add_card=Card.objects.get(c_product_variant=product_variant_obj,c_user=request.user,c_product=product_obj)
                    add_card.quantity=add_card.quantity+quantity
                    add_card.save()
                    request.session['NumberOfCartItems']=request.session['NumberOfCartItems']+quantity
                    
                else: 
                    if product_variant_obj.p_is_sale is True:
                        add_card=Card(c_product_variant=product_variant_obj,c_user=request.user,c_product=product_obj,quantity=quantity,price=product_variant_obj.sale_price)
                    
                    else:
                        add_card=Card(c_product_variant=product_variant_obj,c_user=request.user,c_product=product_obj,quantity=quantity,price=product_variant_obj.price)
                    add_card.save()
                    request.session['NumberOfCartItems']=request.session['NumberOfCartItems']+quantity
                    messages.success(request,'Item added in card successfully')

                return redirect('AtToCard')     
            else:

                return redirect("siginin")
        #product_object=product.objects.get()
        
        card_data=Card.objects.filter(c_user=request.user)
        for card_obj in card_data:

            if card_obj.quantity > card_obj.c_product_variant.quantity:
                difference=card_obj.quantity-card_obj.c_product_variant.quantity

                request.session['NumberOfCartItems']=request.session['NumberOfCartItems']-difference
                card_obj.quantity=card_obj.c_product_variant.quantity
                card_obj.save()

            
        values.update({'card_data':card_data})
        total=0

        for productss in card_data:
            
            if productss.c_product_variant.p_is_sale:

                price=productss.c_product_variant.sale_price*productss.quantity
            else:
                price=productss.c_product_variant.price*productss.quantity

            total=total+price
            
        values.update({'total':total})
        return render(request,'addtocart/addtocart.html',values)
    except Exception as e:
        messages.warning(request,"something went wrong")
        messages.warning(request,e)
        return render(request,'home/notPageFoundError.html')

def delete_card(request,id):
    try:
        record = get_object_or_404(Card,c_id=id)
        quantity=record.quantity
        request.session['NumberOfCartItems']=request.session['NumberOfCartItems']-quantity
        record.delete()
        messages.warning(request,'An item from card deleted successfully')
        return redirect('AtToCard')  
    except Exception as e:
        messages.warning(request,"something went wrong")
        messages.warning(request,e)
        return render(request,'home/notPageFoundError.html')

def NumberOfCartItems_session(request):
    request.session['NumberOfCartItems']=0
    return HttpResponse('NumberOfCartItems is now 0')