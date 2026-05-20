from django.urls import path
from .views import cart,delete_card,NumberOfCartItems_session
urlpatterns = [
    path('',cart,name='AtToCard'),
    path('delete_card/<int:id>',delete_card,name='delete_card'),
    path('NumberOfCartItems_session',NumberOfCartItems_session,name='NumberOfCartItems_session'),
]
