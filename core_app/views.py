from django.shortcuts import render, redirect
from product.models import *


app_name = 'core_app'
# Create your views here.
def IndexView(request):
    product = Product.objects.all()
    context = {
        'product':product,
    }
    return render(request, 'core_app/index.html', context)