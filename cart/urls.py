from django.urls import path 
from .views import *


# app_name = 'cart'

urlpatterns = [
    path('', CartView, name = 'cart'),
    path('add_cart/<int:product_id>/', AddCartView, name = 'add_cart'),
    path('remove_cart/<int:product_id>/', RemoveCartView, name = 'remove_cart'),
    path('remove_cart_item/<int:product_id>/', RemoveCartItemView, name = 'remove_cart_item'),
    
    #checkout urls
    path('checkout/', CheckoutView, name= 'checkout'),
]
