from django.shortcuts import render, redirect
from .models import *


app_name='product'

# Create your views here.
def ProductDetailView(request, id):
    product = Product.objects.get(id=id)
    
    context = {
        'product':product,
    }
    return render(request, 'product/product_detail.html', context)