from django.shortcuts import render, redirect
from product.models import *
from order.models import *



app_name = 'core_app'
# Create your views here.
def IndexView(request):
    orders = Order.objects.filter(
        user=request.user, status__in=["cancelled", "delivered"]
    ).order_by('-created_at')[:5]
    product = Product.objects.all()[:3]
    context = {
        'product':product,
        'orders':orders,
    }
    return render(request, 'core_app/index.html', context)