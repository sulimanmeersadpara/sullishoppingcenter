
from django.urls import path
from .views import add_review,product_reviews
urlpatterns = [
    path('add_review',add_review,name='add_review'),
    path('product_reviews/<id>',product_reviews,name='product_reviews'),
]