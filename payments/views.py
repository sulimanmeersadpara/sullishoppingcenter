from django.shortcuts import render,HttpResponse
from add_to_card.models import Card
from shipping.models import shipping_areas,customer_shipping_location
from django.contrib import messages
from datetime import datetime,timedelta
import hmac
import hashlib
from django.views.decorators.csrf import csrf_exempt

def paymentbutton(request):
    #try:
        JAZZCASH_MERCHANT_ID="MC483531"
        JAZZCASH_PASSWORD="wxy0903u48"
        JAZZCASH_RETURN_URL="http://127.0.0.1:8000/payments/payment_response/"
        JAZZCASH_INTEGRITY_SALT="3uu97153x9"
        card_data=Card.objects.filter(c_user=request.user)
        customerse_place_obj=customer_shipping_location.objects.get(id=int(request.session['customer_shipping_id']))
        context={'card_data':card_data,'customerse_place_obj':customerse_place_obj}
        product_name = 't shirt addidas'
        product_price = customerse_place_obj.advance_pay
        pp_Amount = int(product_price)
        current_datetime = datetime.now()
        pp_TxnDateTime = current_datetime.strftime('%Y%m%d%H%M%S')
        expiry_datetime = current_datetime + timedelta(hours=1)
        pp_TxnExpiryDateTime = expiry_datetime.strftime('%Y%m%d%H%M%S')

        pp_TxnRefNo = "T" + pp_TxnDateTime
        user_id=request.user.id
        
        post_data = {
        "pp_Version": "1.1",
        "pp_TxnType": "MWALLET",
        "pp_Language": "EN",
        "pp_MerchantID": JAZZCASH_MERCHANT_ID,
        "pp_SubMerchantID": "",
        "pp_Password": JAZZCASH_PASSWORD,
        "pp_BankID": "TBANK",
        "pp_ProductID": "RETL",
        "pp_TxnRefNo": pp_TxnRefNo,
        "pp_Amount": pp_Amount,
        "pp_TxnCurrency": "PKR",
        "pp_TxnDateTime": pp_TxnDateTime,
        "pp_BillReference": "billRef",
        "pp_Description": "Description of transaction",
        "pp_TxnExpiryDateTime": pp_TxnExpiryDateTime,
        "pp_ReturnURL": JAZZCASH_RETURN_URL,
        "pp_SecureHash": "",
        "ppmpf_1":user_id,
        "ppmpf_2": request.session['NumberOfCartItems'],
        "ppmpf_3": "3",
        "ppmpf_4": "4",
        "ppmpf_5": "5"
    }

       
        sorted_string = "&".join(f"{key}={value}" for key , value in sorted(post_data.items()) if value != "")
        pp_SecureHash = hmac.new(
        JAZZCASH_INTEGRITY_SALT.encode(),
        sorted_string.encode(),
        hashlib.sha256
        ).hexdigest()
        post_data['pp_SecureHash'] = pp_SecureHash
        
    
        context.update({
					'product_name':product_name,
					'product_price':product_price,
					'post_data':post_data
				})
        return render(request,'payments/paymentbutton.html',context)
    #except Exception as e:
        messages.warning(request,"something went wrong")
        messages.warning(request,e)
        return render(request,'home/notPageFoundError.html')
   



