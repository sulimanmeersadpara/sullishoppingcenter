from . import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from django.conf.urls import handler404
#from .views import custom_404_view  # Import from wherever you placed it

#handler404 = custom_404_view
urlpatterns = [
    path('',include('home.urls')),
    path('categories/',include('categories.urls')),
    path('accounts/',include('accounts.urls')),
    path('products/',include('products.urls')),
    path('cart/',include('add_to_card.urls')),
    path('employee/',include('employee.urls')),
    path('payments/',include('payments.urls')),
    path('admin/', include('admin_app.urls')),
    path('gender_color_size/',include('colorsizegender.urls')),
    path('social_accounts/', include('allauth.urls')),
    path('permissions/', include('permissions.urls')),
    path('shipping_settings/', include('shipping.urls')),
    path('history/', include('history.urls')),
    path('orders/', include('order.urls')),
    path('review/', include('review.urls')),
    path('portfolio/', include('MyPortfolio.urls'))
    
    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)#here may be +=
