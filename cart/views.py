from django.shortcuts import render, redirect, get_object_or_404
from product.models import *
from .models import *
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# app_name = 'cart'

# Create your views here.
def _CartId(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def AddCartView(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Handle quantity (default 1 if not provided)
    quantity = int(request.GET.get('quantity', 1))

    # If user is logged in, use user-based cart
    if request.user.is_authenticated:
        try:
            cart_item = CartItem.objects.get(product=product, user=request.user)
            cart_item.quantity += quantity
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=quantity,
                user=request.user
            )
            cart_item.save()

    else:  # Guest user → use session cart
        try:
            cart = Cart.objects.get(cart_id=_CartId(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id=_CartId(request))
        cart.save()

        try:
            cart_item = CartItem.objects.get(product=product, cart=cart)
            cart_item.quantity += quantity
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=quantity,
                cart=cart
            )
            cart_item.save()

    return redirect('cart')

def RemoveCartView(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_item = get_object_or_404(CartItem, product=product, user=request.user)
    else:    
        cart = Cart.objects.get(cart_id=_CartId(request))
        cart_item = get_object_or_404(CartItem, product=product, cart=cart)
        
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')

def RemoveCartItemView(request, product_id):
    
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=request.user)
    else:    
        cart = Cart.objects.get(cart_id=_CartId(request))
        cart_item = CartItem.objects.get(product=product, cart=cart)
    
    cart_item.delete()
    return redirect('cart')
    

def CartView(request, total=0, quantity=0, cart_item=None):
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.filter(user=request.user, is_active=True)
        else:    
            cart = Cart.objects.get(cart_id=_CartId(request))
            cart_item = CartItem.objects.filter(cart=cart, is_active=True)
            
        for item in cart_item:
            total += (item.product.price * item.quantity)
            quantity += item.quantity
    except :
        pass #just ignore
    
    context = {
        'header_name':'Cart List',
        'total' : total,
        'quantity' : quantity,
        'cart_item' : cart_item,
    }
    return render(request, 'cart/cart.html', context)

