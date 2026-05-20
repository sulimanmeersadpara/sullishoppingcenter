from django.shortcuts import render,redirect,HttpResponse
from .models import Orderhistory
from shipping.models import customer_shipping_location
from add_to_card.models import Card
from order.models import order
from django.contrib import messages
