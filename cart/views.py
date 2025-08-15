from django.shortcuts import render, redirect
from product.models import *
from .models import *
from django.http import HttpResponse

app_name = 'cart'

# Create your views here.
def _CartId(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def AddCartView(request, product_id):
    product = Product.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(cart_id=_CartId(request))#get the cart using the cart id present in the session
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _CartId(request)
        )
    cart.save()
    quantity = int(request.GET.get('quantity', 1))
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart) 
        cart_item.quantity += 1 #cart item.quantity is equal to 1 and we increment it
        cart_item.save()   
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product=product, quantity=quantity, cart=cart
        )
        cart_item.save()
    return redirect('cart:cart')

def CartView(request, total=0, quantity=0, cart_item=None):
    try:
        cart = Cart.objects.get(cart_id=_CartId(request))
        cart_item = CartItem.objects.filter(cart=cart, is_active=True)
        for item in cart_item:
            total += (item.product.price * item.quantity)
            quantity += item.quantity
    except ObjectNotExist:
        pass #just ignore
    
    context = {
        'header_name':'Cart List',
        'total' : total,
        'quantity' : quantity,
        'cart_item' : cart_item,
    }
    return render(request, 'cart/cart.html', context)