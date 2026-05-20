from django.shortcuts import render
from django.http import request,HttpResponse
from products.models import product,gender
from django.core.paginator import Paginator
from categories.models import parent_category
from django.db.models import Q
from django.contrib import messages
from django.db.models import Min, Max
from products.models import product_variant
from order.models import order
from add_to_card.models import Card
from django.db.models import Sum
from review.models import products_review
# Create your views here.
def home(request):
    try:
            data={}
            if request.user.is_authenticated:
                total_qty = Card.objects.filter(c_user=request.user).aggregate(total=Sum('quantity'))['total']
                request.session['NumberOfCartItems']=total_qty
                product_reviews_num=products_review.objects.filter(user=request.user,comment_or_not=0).count()
                data.update({'product_reviews_num':product_reviews_num})
        
            orders=order.objects.filter(admin_read_status=0).count()
                    
            if request.GET.get('page'):
                page_number=request.GET.get('page') #this will come in url
        
            else:
                page_number='1'

            
            
            if request.GET.get('PriceRange') and not request.GET.get('gender'):
                
                priceRange=request.GET.get('PriceRange')
                if 'gender' in request.session:
                    #products=product.objects.filter(max_price__lte=priceRange,p_gender=request.session['gender']).order_by('-max_price')
                    
                    products = product.objects.filter(
                    (
                    Q(max_price__lte=priceRange) | Q(min_price__lte=priceRange)
                    ) &
                    Q(p_gender=request.session['gender'])
                    ).order_by('-max_price')

                    # # products = product.objects.annotate(
                    # # min_price=Min('product_product_variant__price')
                    # # ).filter(
                    #     min_price__lte=priceRange,
                    #      p_gender_id=request.session['gender']
                    #          )
                else:
                    
                    #products=product.objects.filter(max_price__lte=priceRange).order_by('-max_price')
                    products = product.objects.filter(
                    (
                    Q(max_price__lte=priceRange) | Q(min_price__lte=priceRange)
                    ) 
                    ).order_by('-max_price')

                    # products = product.objects.annotate(
                    # min_price=Min('product_product_variant__price')
                    # ).filter(min_price__lte=priceRange)
                
                priceRange=int(priceRange)
                data.update({'priceRange':priceRange})
                
            
            elif request.GET.get('PriceRange') and request.GET.get('gender'):
                
                priceRange=int(request.GET.get('PriceRange'))
                gender_id=int(request.GET.get('gender'))
                if(gender_id is -1):
            
                    #products=product.objects.filter(max_price__lte=priceRange).order_by('-max_price')
                    products = product.objects.filter(
                    (
                    Q(max_price__lte=priceRange) | Q(min_price__lte=priceRange)
                    )
                    ).order_by('-max_price')

                    # products = product.objects.annotate(
                    # min_price=Min('product_product_variant__price')
                    # ).filter(min_price__lte=priceRange)
                    if 'gender' in request.session:
                        del request.session['gender']
                    
                
                else:
                    #products=product.objects.filter(max_price__lte=priceRange,p_gender=gender_id).order_by('-max_price')
                    products = product.objects.filter(
                    (
                    Q(max_price__lte=priceRange) | Q(min_price__lte=priceRange)
                    ) &
                    Q(p_gender=gender_id)
                    ).order_by('-max_price')

                    # # products = product.objects.annotate(
                    # # min_price=Min('product_product_variant__price')
                    # # ).filter(
                    #     min_price__lte=priceRange,
                    #     p_gender=gender_id
                    #          )
                    priceRange=int(priceRange)
                    request.session['gender']=gender_id
                
                data.update({'priceRange':priceRange})
                
            elif(request.GET.get('gender') or 'gender' in request.session):
                if request.GET.get('gender'):
                
                
                    gender_id=int(request.GET.get('gender'))

                else:
                    gender_id=request.session['gender']
                if(gender_id is -1):
                    
                    products=product.objects.all()
                    if('gender' in request.session):
                        del request.session['gender']
                else:
                    
                    products=product.objects.filter(p_gender=gender_id)
                    request.session['gender']=gender_id
            else:
                products=product.objects.all()
            
            if products:
                p=Paginator(products,16) #every page will show 2 records
                ServiceDatafinal=p.get_page(page_number) #it will return the two records to display in page
                totalpage=ServiceDatafinal.paginator.num_pages #it will return how much pages can be create from compairing/dividing the number of records and number should display for one page
                #return HttpResponse(ServiceDatafinal)
                data.update({
                'page_no':int(page_number),
                'serviceData':ServiceDatafinal,
                'lastpage':totalpage,
                'totalPagelist':[n+1 for n in range(totalpage)]
                })
                #return HttpResponse(products)
                categories=parent_category.objects.all()
                data.update({'categories':categories})
                genders=gender.objects.all()
                data.update({'genders':genders})
                
                price_range = product.objects.aggregate(
                overall_min_price=Min('min_price'),
                overall_max_price=Max('max_price')
                )

            # Example usage
                min_price = price_range['overall_min_price']
                max_price = price_range['overall_max_price']
                
                pricelist=[]
                
                gap=int((max_price-min_price)/5) # because we want to bring only 14 values to display in home page
                if gap is not 0:
                    for k in range(min_price,max_price,gap):
                        r=k%100
                        s=100-r
                        prce=k+s
                        pricelist.append(prce)

                    if pricelist:
                        pricelist.pop()
                    r=max_price%gap
                    s=gap-r
                    prce=max_price+s
                    pricelist.append(prce)
                    data.update({'max_price':max_price})
                    data.update({'pricelist':pricelist})
                if 'search' in request.session:
                    del request.session['search']
                request.session['path']=request.path
            else:
                noProductFoundError=True
                data.update({'noProductFoundError':noProductFoundError})
            
            data.update({'orders':orders})
            return render(request,"home/home.html",data)
    except Exception as e:
        messages.warning(request,"something went wrong")
        messages.warning(request,e)
        return render(request,'home/notPageFoundError.html')
        
    


def check_session(request):
    return render(request,'home/check_session.html')
def search(request):
    try:
        data={}
        if request.GET.get('page'):
            page_number=request.GET.get('page') #this will come in url
        else:
            page_number='1' 
        if request.method=="POST":
            search_query=request.POST['search']
            request.session['search']=search_query
        else:
            search_query=request.session['search']
        if request.GET.get('gender'):
            gender_id=int(request.GET.get('gender'))
            if gender_id is -1:
                if 'gender' in request.session:
                    del request.session['gender']
                products=product.objects.filter(Q(p_name__icontains=search_query)|Q(p_description__icontains=search_query)|Q(p_compony__icontains=search_query))
            else:
                products=product.objects.filter(Q(p_name__icontains=search_query)|Q(p_description__icontains=search_query)|Q(p_compony__icontains=search_query),p_gender=gender_id)
                request.session['gender']=gender_id
        else:
            products=product.objects.filter(Q(p_name__icontains=search_query)|Q(p_description__icontains=search_query)|Q(p_compony__icontains=search_query))
        p=Paginator(products,18) #every page will show 2 records
        ServiceDatafinal=p.get_page(page_number) #it will return the two records to display in page
        totalpage=ServiceDatafinal.paginator.num_pages #it will return how much pages can be create from compairing/dividing the number of records and number should display for one page
        #return HttpResponse(ServiceDatafinal)
        data.update({
            'page_no':int(page_number),
            'serviceData':ServiceDatafinal,
            'lastpage':totalpage,
            'totalPagelist':[n+1 for n in range(totalpage)]
            })
        categories=parent_category.objects.all()
        data.update({'categories':categories})
        genders=gender.objects.all()
        data.update({'genders':genders})
        #return HttpResponse(products)
        
        request.session['path']=request.path
        return render(request,"home/search.html",data)
    except Exception as e:
        messages.warning(request,"something went wrong")
        messages.warning(request,e)
        return render(request,'home/notPageFoundError.html')

