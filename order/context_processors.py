from .models import Order
from django.db.models import Q

def pending_orders_count(request):
    if request.user.is_authenticated:
        count = Order.objects.filter(
            user=request.user
        ).filter(
            Q(status="pending") | Q(status="processing")
        ).count()
    else:
        count = 0
    return {
        "pending_orders_count": count
    }
