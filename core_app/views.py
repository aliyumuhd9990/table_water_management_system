from django.shortcuts import render, redirect
from product.models import *
from order.models import *



app_name = 'core_app'
# Create your views here.

def IndexView(request):
    # Always fetch products
    product = Product.objects.all()[:3]
    groups = request.user.staff_groups.all() if request.user.is_authenticated else None

    # Only fetch orders if the user is logged in
    if request.user.is_authenticated:
        orders = Order.objects.filter(
            user=request.user, status__in=["cancelled", "delivered"]
        ).order_by('-created_at')[:5]
    else:
        orders = []  # anonymous visitors

    context = {
        'product': product,
        'orders': orders,
        "groups": groups,
    }
    return render(request, 'core_app/index.html', context)
