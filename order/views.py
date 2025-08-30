from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from cart.models import *
from .models import *
from accounts.models import *
from django.contrib import messages
from django.http import HttpResponse
from cart.views import _CartId

from .utils import assign_driver_to_order
#for generating pdf
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from django.http import HttpResponse


@login_required(login_url='login')
def CreateOrderView(request):
    user = request.user
    cart_items = CartItem.objects.filter(user=request.user, is_active=True)
    if not cart_items.exists():
        return redirect('cart')

    total = sum(item.product.price * item.quantity for item in cart_items)

    if request.method == "POST":
        full_name = request.POST['full_name']
        email = request.POST['email']
        address = request.POST['address']
        address2 = request.POST['address2']
        lga = request.POST.get("state")  # will match choices now
        phone = request.POST['phone']

        if phone == "080xxxxxx":
            messages.error(request, 'Update Your Contact')
            return redirect(reverse('create_order'))

        # ✅ Find driver for selected LGA
        driver_route = DriverRoute.objects.filter(lga=lga).first()
        driver = driver_route.driver if driver_route else None

        # ✅ Create order
        order = Order.objects.create(
            user=user,
            full_name=full_name,
            email=email,
            address=address,
            address2=address2,
            phone=phone,
            total_price=total,
            lga=lga,
            status="pending"  # only pending until paid
        )

        # ✅ Create order items
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
            item.delete()

        return redirect('payment:initialize_payment', order_id=order.id)


    context = {
        'header_name': 'Create Order Page',
        'cart_items': cart_items,
        'total': total,
        'user': user,
        # 'quantity': quantity,
    }
    return render(request, 'order/checkout.html', context)

@login_required(login_url='login')
def OrderSuccessView(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user)
    
    context = {
        'header_name': 'Order Success Page',
        'order': order,
    }
    return render(request, 'order/order_success.html', context)


@login_required(login_url='login')
def OrderListView(request):
    orders = Order.objects.filter(
        user=request.user, status__in=["cancelled", "delivered"]
    ).order_by('-created_at')
    print(Order.objects.filter(user=request.user).values_list("id", "status"))

    context = {
        'header_name': 'Order History',
        'orders': orders,
    }
    return render(request, 'order/order_history.html', context)

@login_required(login_url='login')
def PendingOrdersView(request):
    orders = Order.objects.filter(
        user=request.user, status__in=["pending", "assigned"]
    ).order_by('-created_at')
    
    context = {
        'header_name': 'Pending Orders',
        'orders': orders,
    }
    return render(request, 'order/pending_orders.html', context)

@login_required(login_url='login')
def InvoiceView(request, invoice_id): 
    user = request.user
    # Fetch order for logged-in user
    order = get_object_or_404(Order, id=invoice_id, user=request.user)

    # Fetch items (thanks to related_name="items")
    items = order.items.all()
   
     # Example invoice data
    customer = {
    "name": user.full_name,
    "email": user.email,
    "phone": order.phone,
    "status": "Paid" if order.paid else "Pending"
}

     # Calculate totals
    products = []
    for item in items:
        total = item.quantity * item.price
        products.append({
            "name": item.product.pname,
            "qty": item.quantity,
            "price": item.price,
            "total": total,
        })

    # Calculate totals
    for p in products:
        p["total"] = p["qty"] * p["price"]

    grand_total = sum(p["total"] for p in products)

    # Prepare response
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f"inline; filename=invoice_{invoice_id}.pdf"

    # Create PDF document
    doc = SimpleDocTemplate(response, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    # Invoice header
    elements.append(Paragraph(f"<b>Invoice #01{invoice_id}92</b>", styles["Title"]))
    elements.append(Spacer(1, 12))

    # Customer info
    customer_info = f"""
        <b>Customer Name:</b> {customer['name']} <br/><br/>
        <b>Email:</b> {customer['email']} <br/><br/>
        <b>Phone:</b> {customer['phone']} <br/><br/>
        <b>Status:</b> {customer['status']} <br/><br/>
    """
    elements.append(Paragraph(customer_info, styles["Normal"]))
    elements.append(Spacer(1, 20))

    # Table data (header + rows)
    data = [["Product", "Quantity", "Price", "Total"]]
    for p in products:
        data.append([p["name"], p["qty"], f"N{p['price']}", f"N{p['total']}"])
    data.append(["", "", "Grand Total", f"N{grand_total}"])

    # Create table
    table = Table(data, colWidths=[200, 80, 80, 100])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
        ("ALIGN", (1, 1), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BACKGROUND", (0, -1), (-1, -1), colors.lightgrey),
    ]))
    elements.append(table)

    # Build PDF
    doc.build(elements)
    return response

@login_required
def driver_orders(request):
    driver = request.user  # assuming driver is logged in
    assigned_orders = Order.objects.filter(driver=driver, status="assigned").count()
    delivering_orders = Order.objects.filter(driver=driver, status="delivering").count()
    delivered_orders = Order.objects.filter(driver=driver, status="delivered").count()
    
    if request.user.role == "staff" and request.user.staff_groups.filter(name="A").exists():
        orders = Order.objects.filter(driver=request.user).exclude(status="delivered")
        
        context = {
            'header_name': '🚚 My Assigned Orders',
            "orders": orders,
            "assigned_orders": assigned_orders,
            "delivering_orders": delivering_orders,
            "delivered_orders": delivered_orders,
        }
        return render(request, "order/driver_orders.html", context)
    return redirect("index")

@login_required
def update_status(request, order_id):
    order = get_object_or_404(Order, id=order_id, driver=request.user)

    if request.method == "POST":
        status = request.POST.get("status")
        if status in ["delivering", "delivered"]:
            order.status = status
            order.save()
    return redirect("driver_orders")