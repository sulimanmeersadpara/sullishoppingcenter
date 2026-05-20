from django.shortcuts import render, HttpResponse,redirect
from django.core.mail import EmailMultiAlternatives
from email.mime.image import MIMEImage
import os
from shipping.models import customer_shipping_location
from add_to_card.models import Card
from django.contrib import messages
def send_order_confirmation_email(request):
  try:
      try:
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        customer_shipping_obj=customer_shipping_location.objects.get(user_id=request.user)
        total_price=customer_shipping_obj.total    
        delivery_code = request.session.get('delveiry_code')
        card_data=Card.objects.filter(c_user=request.user)
        order_items = []
        for c in card_data:
            image_name=c.c_product_variant.product_variant.first().image
            order_items.append({
            "name": c.c_product_variant.size.size_name+' - '+c.c_product_variant.color.color_name+' - '+c.c_product.p_name ,
            "qty": c.quantity,
            "price": c.price,
            "image_path": os.path.join(BASE_DIR, f"media/images/{image_name}")
        })


        subject = "🛍️ Order Confirmed - Sulli Shopping Center"
        from_email = "sullisoppingcenter@gmail.com"
        to = [request.user.email,'salmanmeergabbar@gmail.com']
        text_content = "Your order has been confirmed!"

        # --- Build HTML dynamically ---
        product_html = ""
        for i, item in enumerate(order_items):
            cid = f"product_image_{i}"
            
            product_html += f"""
            <tr style="border-bottom:1px solid #ddd;">
              <td style="padding:10px; text-align:center;">
                <img src="cid:{cid}" width="100" style="border-radius:10px;">
              </td>
              <td style="padding:10px;">{item['name']}</td>
              <td style="padding:10px;">{item['qty']}</td>
              <td style="padding:10px;">Rs {item['price']}</td>
            </tr>
            """

        html_content = f"""
        <html>
          <body style="font-family:Arial,sans-serif; color:#333;">
            <h2 style="color:#4CAF50;">Order Confirmation</h2>
            <p>Dear Customer,</p>
            <p>Thank you for shopping with <b>Sulli Shopping Center</b>!</p>

            <table style="width:100%; border-collapse:collapse; margin-top:20px;">
              <tr style="background-color:#f2f2f2;">
                <th style="padding:10px;">Product</th>
                <th style="padding:10px;">Name</th>
                <th style="padding:10px;">Qty</th>
                <th style="padding:10px;">Price</th>
              </tr>
              {product_html}
            </table>

            <h3 style="text-align:right; margin-top:20px;">Total: Rs {total_price}</h3>
            <h4 style="text-align:right; margin-top:20px; color:rgb(131, 131, 131)">your delvery code is :  {delivery_code}</h4>
            <i>the delevery boy will ask for this number</i>
            
            <p style="margin-top:30px;">The products will deliver in your address <b>{customer_shipping_obj.address1} {customer_shipping_obj.address2} {customer_shipping_obj.shipping_area_id.city.city_name}</b> within {customer_shipping_obj.shipping_area_id.estimated_time}
                </i></p>
            <p>Thank you,<br><b>Sulli Shopping Center</b></p>
          </body>
        </html>
        """

        # Create and send email
        msg = EmailMultiAlternatives(subject, text_content, from_email, to)
        msg.attach_alternative(html_content, "text/html")

        # Attach each image as embedded content
        for i, item in enumerate(order_items):
            cid = f"product_image_{i}"
            image_path = item["image_path"]
            with open(image_path, "rb") as img:
                image = MIMEImage(img.read())
                image.add_header("Content-ID", f"<{cid}>")
                msg.attach(image)

        msg.send()
      except Exception as e:
        messages.warning(request,"oop! the email for confirmation couldnot send")
        messages.warning(request,e)
        return redirect('paymentbutton')
        
    
      delete_card(request)
      
      return redirect('success_checkout')
  except Exception as e:
        messages.warning(request,"something went wrong")
        messages.warning(request,e)
        return render(request,'home/notPageFoundError.html')
        
def delete_card(request):
    try:
        
        records=Card.objects.filter(c_user=request.user)
        for record in records:
            record.delete()
        request.session['NumberOfCartItems']=0
        
       
    except Exception as e:
        messages.warning(request,"something went wrong")
        messages.warning(request,e)
        return render(request,'home/notPageFoundError.html')
   