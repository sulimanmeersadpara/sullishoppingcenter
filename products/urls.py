
from django.contrib import admin
from django.urls import path
from .views import add_products
from .views2 import get_products,product_list
from .views3 import update_products,delete_products
from .views4 import images,delete_images
from .views5 import product_variants_menpulation,delete_variantFunc,add_new_variant
from .views6 import product_variant_update
urlpatterns = [
    path('manipulations',product_list ,name='manipulation'),
    path('update_product/<slug>/',update_products ,name='update_product'),
    path('delete_products/<slug>',delete_products ,name='delete_products'),
    path('add_products',add_products ,name='add_products'),
    path('add_new_variant/<slug>',add_new_variant ,name='add_new_variant'),
    path('product_variant_update/<pv_id>',product_variant_update ,name='product_variant_update'),
    path('product_variant/<slug>',product_variants_menpulation,name="product_variants_menpulation"),
    path('delete_variant/<slug>/<pv_id>',delete_variantFunc,name="delete_variant"),
    path('images/<slug>/<pv_id>/',images,name="images"),
    path('delete_images/<id>',delete_images,name="delete_images"),
    path('<slug>/',get_products,name="products_detail"),
    path('admin/', admin.site.urls),
]
