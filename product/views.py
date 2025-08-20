from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from cart.models import *
from cart.views import _CartId

app_name='product'

# Create your views here.
def ProductListView(request):
    product = Product.objects.all()
    
    context = {
        'header_name' : 'Product List',
        'product' : product,
    }
    return render(request, 'product/product.html', context)

def ProductDetailView(request, id):
    try:
        product = get_object_or_404(Product, id=id)
        in_cart = CartItem.objects.filter(cart__cart_id=_CartId(request), product=product)
    except Exception as e:
        raise e
    
    context = {
        'product':product,
        'in_cart' : in_cart,
        'header_name' : 'Pack Detail',
    }
    return render(request, 'product/product_detail.html', context)