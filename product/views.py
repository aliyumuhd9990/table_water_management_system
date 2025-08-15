from django.shortcuts import render, redirect, get_object_or_404
from .models import *


app_name='product'

# Create your views here.
def ProductDetailView(request, id):
    product = get_object_or_404(Product, id=id)
    
    context = {
        'product':product,
        'header_name' : 'Pack Detail',
    }
    return render(request, 'product/product_detail.html', context)