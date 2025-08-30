# import braintree
import requests
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from order.models import *
# from xhtml2pdf import pisa
from io import BytesIO
from .models import *
from django.contrib.auth.decorators import login_required
# from django.template.loader import render_to_string
# from weasyprint import HTML
# from django.http import HttpResponse
from django.contrib import messages
# Crimport braintree
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from cart.models import *


app_name = 'payment'

def initialize_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    total_price = order.total_price
    
    # cart_item = CartItem.objects.filter(user=request.user, is_active=True)
    
    # total = 0
    # for item in cart_item:
        # total += item.sub_total() 
      
    amount = int(total_price * 100)  # Paystack uses Kobo

    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "email": request.user.email,
        "amount": amount,
        "callback_url": request.build_absolute_uri('/payment/verify/'),
    }

    url = "https://api.paystack.co/transaction/initialize"
    response = requests.post(url, json=data, headers=headers)
    res = response.json()

    if res['status']:
        reference = res['data']['reference']
        Payment.objects.create(
            user=request.user,
            order=order,
            amount=amount,
            reference=reference
        )

        return redirect(res['data']['authorization_url'])
    else:
        return redirect('payment:canceled')

# views.py
def verify_payment(request):
    reference = request.GET.get('reference')

    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
    }
    url = f"https://api.paystack.co/transaction/verify/{reference}"

    response = requests.get(url, headers=headers)
    res = response.json()

    if res['status'] and res['data']['status'] == 'success':
        payment = get_object_or_404(Payment, reference=reference)
        payment.verified = True
        payment.save()

        # Mark the order as Paid
        order = payment.order
        order.paid = True
        order.save()
        
          # ✅ assign driver now that it’s paid
        driver = assign_driver_to_order(order)

        if driver:
            messages.success(request, f"Order paid and assigned to driver {driver.full_name}.")
        else:
            messages.warning(request, "Order paid but no driver available right now.")


        return redirect('payment:done', order_id=order.id)
    return redirect('payment:canceled')

def payment_done(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user)
    
    context = {
        'header_name': 'Order Success Page',
        'order': order,
    }
    return render(request, 'payment/payment_done.html', context)

@login_required(login_url='login')
def payment_canceled(request):
    # return redirect(reverse('products:invoice_detail', ))
    return render(request, 'payment/canceled.html')

def assign_driver_to_order(order):
    # find driver for order LGA
    driver_route = DriverRoute.objects.filter(lga=order.lga).first()
    if driver_route:
        order.driver = driver_route.driver
        order.status = "assigned"
        order.save()
        return driver_route.driver
    return None