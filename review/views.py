from django.shortcuts import render,HttpResponse
from review.models import products_review
from products.models import product
def add_review(request):
    
    product_reviews=products_review.objects.filter(user=request.user)
    if request.method=='POST':
        id=request.POST['id']
        star=int(request.POST['stars'])
        comment=request.POST['comment']
        pr_record=products_review.objects.get(id=id)
        pr_record.comment=comment
        pr_record.star_rate=star
        pr_record.comment_or_not=1
        pr_record.save()
        pr_record.c_product.average_star_rate=((pr_record.c_product.average_star_rate * pr_record.c_product.rate_persons)+pr_record.star_rate)/(pr_record.c_product.rate_persons+1)
        pr_record.c_product.rate_persons+=1
        pr_record.c_product.save()        
    return render(request,'review/add_review.html',{'product_reviews':product_reviews})

# Create your views here.
def product_reviews(request, id):
    product_obj=product.objects.get(p_id=id)
    
    product_reviews=products_review.objects.filter(c_product=product_obj)
    
    return render(request,'review/product_reviews.html',{'product_reviews':product_reviews})