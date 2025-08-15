from django.urls import path 
from .views import *


app_name = 'cart'
urlpatterns = [
    path('', CartView, name = 'cart'),
    path('add_cart/<int:product_id>/', AddCartView, name = 'add_cart'),
    
]
